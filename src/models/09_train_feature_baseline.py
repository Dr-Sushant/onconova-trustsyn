from pathlib import Path
import argparse
import pandas as pd

import joblib
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error

from scipy.stats import pearsonr

from xgboost import XGBRegressor

from src.utils.merge_features import (
    merge_drug_features,
    merge_cell_features,
    merge_pair_features,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# -------------------------------------------------------
# Arguments
# -------------------------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument(
    "--split",
    default="random",
    choices=["random", "cold_drug", "cold_cell", "cold_pair"],
)

parser.add_argument(
    "--feature_table",
    required=True,
    help="Feature table inside data/features/",
)

parser.add_argument(
    "--feature_type",
    required=True,
    choices=["drug", "cell", "pair"],
)

args = parser.parse_args()


# -------------------------------------------------------
# Paths
# -------------------------------------------------------

TRAIN = PROJECT_ROOT / "splits" / args.split / "train.csv"
VALID = PROJECT_ROOT / "splits" / args.split / "valid.csv"

FEATURE_TABLE = PROJECT_ROOT / "data" / "features" / args.feature_table

FEATURE_NAME = Path(args.feature_table).stem

RESULTS_DIR = (
    PROJECT_ROOT / "results" / "benchmark" / "xgboost" / FEATURE_NAME / args.split
)

MODEL_DIR = PROJECT_ROOT / "models" / "benchmark" / "xgboost" / FEATURE_NAME

MODEL_DIR.mkdir(parents=True, exist_ok=True)

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------
# Load
# -------------------------------------------------------

train = pd.read_csv(TRAIN)
valid = pd.read_csv(VALID)
feature_df = pd.read_csv(FEATURE_TABLE)

if args.feature_type == "drug":

    train, valid, feature_cols = merge_drug_features(
        train,
        valid,
        feature_df,
    )

elif args.feature_type == "cell":

    train, valid, feature_cols = merge_cell_features(
        train,
        valid,
        feature_df,
    )

elif args.feature_type == "pair":

    train, valid, feature_cols = merge_pair_features(
        train,
        valid,
        feature_df,
    )

else:

    raise ValueError(f"Unknown feature type: {args.feature_type}")


print("\nMerged successfully")
print("Train:", train.shape)
print("Valid:", valid.shape)
print("Number of merged features:", len(feature_cols))

# -------------------------------------------------------
# Build feature matrix
# -------------------------------------------------------

if args.feature_type == "drug":

    le = LabelEncoder()

    all_cells = pd.concat([train["CELLNAME"], valid["CELLNAME"]])

    le.fit(all_cells)

    train["cell"] = le.transform(train["CELLNAME"])
    valid["cell"] = le.transform(valid["CELLNAME"])

    feature_cols = ["cell"] + feature_cols

elif args.feature_type == "cell":

    # Cell features are already merged on CELLNAME
    pass

elif args.feature_type == "pair":

    # Pair features will already be merged
    pass

X_train = train[feature_cols]
X_valid = valid[feature_cols]

y_train = train["combo_score"]
y_valid = valid["combo_score"]

print("\nFeature matrix")
print("X_train:", X_train.shape)
print("X_valid:", X_valid.shape)

print("\nMissing values")
print("Train:", X_train.isna().sum().sum())
print("Valid:", X_valid.isna().sum().sum())

X_train = X_train.fillna(0)
X_valid = X_valid.fillna(0)

# -------------------------------------------------------
# Train model
# -------------------------------------------------------

model = XGBRegressor(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1,
)

print("\nTraining model...")

model.fit(X_train, y_train)

print("Training complete.")

# -------------------------------------------------------
# Prediction
# -------------------------------------------------------

pred = model.predict(X_valid)

# -------------------------------------------------------
# Metrics
# -------------------------------------------------------

rmse = np.sqrt(mean_squared_error(y_valid, pred))
mae = mean_absolute_error(y_valid, pred)
pearson = pearsonr(y_valid, pred)[0]

print("\n===============================")
print("BENCHMARK RESULTS")
print("===============================")

print(f"RMSE     : {rmse:.4f}")
print(f"MAE      : {mae:.4f}")
print(f"Pearson  : {pearson:.4f}")

# -------------------------------------------------------
# Save predictions
# -------------------------------------------------------

pred_df = pd.DataFrame(
    {
        "Actual": y_valid,
        "Predicted": pred,
    }
)

pred_df.to_csv(
    RESULTS_DIR / "predictions.csv",
    index=False,
)

# -------------------------------------------------------
# Save metrics
# -------------------------------------------------------

metrics_df = pd.DataFrame(
    {
        "Metric": ["RMSE", "MAE", "Pearson"],
        "Value": [rmse, mae, pearson],
    }
)

metrics_df.to_csv(
    RESULTS_DIR / "metrics.csv",
    index=False,
)

# -------------------------------------------------------
# Save model
# -------------------------------------------------------

joblib.dump(
    model,
    MODEL_DIR / f"{args.split}.pkl",
)

print("\nSaved to")
print(RESULTS_DIR)

# print("=" * 60)
# print("Split :", args.split)
# print("Feature :", args.feature_table)
# print("Type :", args.feature_type)
# print("=" * 60)

# print("\nTrain:", train.shape)
# print("Valid:", valid.shape)
# print("Feature:", feature_df.shape)

# print("\nColumns:\n")
# print(feature_df.columns.tolist()[:20])
