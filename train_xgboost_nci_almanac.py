from pathlib import Path
import json
import warnings

import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from scipy.stats import pearsonr

from xgboost import XGBRegressor

warnings.filterwarnings("ignore")


# =============================================================================
# CONFIGURATION
# =============================================================================

ROOT = Path(r"D:\Novartis\onconova-trustsyn")

SPLITS_ROOT = ROOT / "extra" / "_extracted" / "anoushka_splits" / "splits"

OUTPUT_ROOT = ROOT / "results" / "benchmark" / "xgboost" / "nci_almanac_62f"

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

TARGET = "combo_score"

SEED = 42


# =============================================================================
# EXACT FROZEN 62-FEATURE SET
# =============================================================================

FEATURES = [f"CellMiner_PC{i}" for i in range(1, 51)] + [
    "STRING_distance",
    "STRING_available",
    "KEGG_overlap",
    "Tanimoto_similarity",
    "target_count_A",
    "target_count_B",
    "shared_target_count",
    "union_target_count",
    "target_jaccard",
    "target_overlap_A",
    "target_overlap_B",
    "has_shared_target",
]


assert len(FEATURES) == 62


# =============================================================================
# HELPERS
# =============================================================================


def calculate_metrics(y_true, y_pred):

    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    mae = mean_absolute_error(y_true, y_pred)

    r2 = r2_score(y_true, y_pred)

    pearson_r, pearson_p = pearsonr(y_true, y_pred)

    return {
        "RMSE": float(rmse),
        "MAE": float(mae),
        "Pearson_r": float(pearson_r),
        "Pearson_p": float(pearson_p),
        "R2": float(r2),
    }


def load_split(path):

    df = pd.read_csv(path)

    if TARGET not in df.columns:
        raise RuntimeError(f"{path} does not contain target '{TARGET}'")

    missing = [f for f in FEATURES if f not in df.columns]

    if missing:
        raise RuntimeError(
            f"{path} is missing {len(missing)} " f"required features:\n{missing}"
        )

    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    # Explicit numeric conversion
    for col in FEATURES:
        X[col] = pd.to_numeric(X[col], errors="raise")

    y = pd.to_numeric(y, errors="raise")

    if X.isna().any().any():
        nan_cols = X.columns[X.isna().any()].tolist()

        raise RuntimeError(f"NaNs detected in {path}: " f"{nan_cols}")

    if y.isna().any():
        raise RuntimeError(f"NaNs detected in target: {path}")

    return df, X, y


def find_split_directories():

    directories = []

    for d in sorted(SPLITS_ROOT.iterdir()):

        if not d.is_dir():
            continue

        train = d / "train.csv"
        val = d / "val.csv"
        test = d / "test.csv"

        if train.exists() and val.exists() and test.exists():
            directories.append(d)

    return directories


# =============================================================================
# DISCOVER SPLITS
# =============================================================================

print("=" * 90)
print("NCI-ALMANAC XGBOOST — FROZEN 62-FEATURE BENCHMARK")
print("=" * 90)

print("\nSplits root:")
print(SPLITS_ROOT)

split_dirs = find_split_directories()

if not split_dirs:
    raise RuntimeError("No train/val/test split directories found.")

print("\nDiscovered split sets:")

for d in split_dirs:
    print("  ", d.name)

print("\nNumber of split sets:", len(split_dirs))


# =============================================================================
# FEATURE AUDIT
# =============================================================================

print("\n" + "=" * 90)
print("FEATURE AUDIT")
print("=" * 90)

print("\nFeature count:", len(FEATURES))

print("\nCellMiner:")
print("  50 PCs")

print("\nPair/network:")
for f in FEATURES[50:]:
    print(" ", f)


# =============================================================================
# MODEL CONFIGURATION
# =============================================================================

MODEL_PARAMS = {
    "n_estimators": 1000,
    "max_depth": 8,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "objective": "reg:squarederror",
    "eval_metric": "rmse",
    "random_state": SEED,
    "n_jobs": -1,
    "tree_method": "hist",
}


# =============================================================================
# TRAIN EACH SPLIT
# =============================================================================

all_results = []


for split_dir in split_dirs:

    split_name = split_dir.name

    print("\n\n" + "#" * 90)
    print("SPLIT:", split_name)
    print("#" * 90)

    train_path = split_dir / "train.csv"
    val_path = split_dir / "val.csv"
    test_path = split_dir / "test.csv"

    # -------------------------------------------------------------------------
    # LOAD
    # -------------------------------------------------------------------------

    train_df, X_train, y_train = load_split(train_path)

    val_df, X_val, y_val = load_split(val_path)

    test_df, X_test, y_test = load_split(test_path)

    print("\nShapes:")
    print("  Train:", X_train.shape)
    print("  Val  :", X_val.shape)
    print("  Test :", X_test.shape)

    assert X_train.shape[1] == 62
    assert X_val.shape[1] == 62
    assert X_test.shape[1] == 62

    # -------------------------------------------------------------------------
    # MODEL
    # -------------------------------------------------------------------------

    model = XGBRegressor(
        **MODEL_PARAMS,
        early_stopping_rounds=50,
    )

    print("\nTraining XGBoost...")

    model.fit(
        X_train,
        y_train,
        eval_set=[
            (X_train, y_train),
            (X_val, y_val),
        ],
        verbose=False,
    )

    # -------------------------------------------------------------------------
    # PREDICTIONS
    # -------------------------------------------------------------------------

    train_pred = model.predict(X_train)

    val_pred = model.predict(X_val)

    test_pred = model.predict(X_test)

    # -------------------------------------------------------------------------
    # METRICS
    # -------------------------------------------------------------------------

    train_metrics = calculate_metrics(y_train, train_pred)

    val_metrics = calculate_metrics(y_val, val_pred)

    test_metrics = calculate_metrics(y_test, test_pred)

    print("\nBest iteration:")
    print(getattr(model, "best_iteration", None))

    print("\nTRAIN")
    for k, v in train_metrics.items():
        print(f"  {k:12s}: {v:.6f}")

    print("\nVALIDATION")
    for k, v in val_metrics.items():
        print(f"  {k:12s}: {v:.6f}")

    print("\nTEST")
    for k, v in test_metrics.items():
        print(f"  {k:12s}: {v:.6f}")

    # -------------------------------------------------------------------------
    # SAVE PREDICTIONS
    # -------------------------------------------------------------------------

    out_dir = OUTPUT_ROOT / split_name
    out_dir.mkdir(parents=True, exist_ok=True)

    predictions = test_df[
        [
            c
            for c in [
                "drug_A",
                "drug_B",
                "CELLNAME",
                "combo_score",
            ]
            if c in test_df.columns
        ]
    ].copy()

    predictions["prediction"] = test_pred
    predictions["residual"] = predictions[TARGET] - predictions["prediction"]

    predictions.to_csv(out_dir / "test_predictions.csv", index=False)

    # -------------------------------------------------------------------------
    # SAVE METRICS
    # -------------------------------------------------------------------------

    result = {
        "split": split_name,
        "n_train": len(X_train),
        "n_val": len(X_val),
        "n_test": len(X_test),
        "n_features": len(FEATURES),
        "best_iteration": int(getattr(model, "best_iteration", -1)),
        "train_RMSE": train_metrics["RMSE"],
        "train_MAE": train_metrics["MAE"],
        "train_Pearson_r": train_metrics["Pearson_r"],
        "train_R2": train_metrics["R2"],
        "val_RMSE": val_metrics["RMSE"],
        "val_MAE": val_metrics["MAE"],
        "val_Pearson_r": val_metrics["Pearson_r"],
        "val_R2": val_metrics["R2"],
        "test_RMSE": test_metrics["RMSE"],
        "test_MAE": test_metrics["MAE"],
        "test_Pearson_r": test_metrics["Pearson_r"],
        "test_R2": test_metrics["R2"],
    }

    all_results.append(result)

    with open(out_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    # -------------------------------------------------------------------------
    # SAVE MODEL
    # -------------------------------------------------------------------------

    model.save_model(out_dir / "xgboost_model.json")


# =============================================================================
# FINAL SUMMARY
# =============================================================================

summary = pd.DataFrame(all_results)

summary_path = OUTPUT_ROOT / "summary.csv"

summary.to_csv(summary_path, index=False)

print("\n\n" + "=" * 90)
print("FINAL XGBOOST BENCHMARK")
print("=" * 90)

print(
    summary[
        [
            "split",
            "n_train",
            "n_val",
            "n_test",
            "test_RMSE",
            "test_MAE",
            "test_Pearson_r",
            "test_R2",
            "best_iteration",
        ]
    ].to_string(index=False)
)

print("\nSaved:")
print(summary_path)

print("\nDONE.")
