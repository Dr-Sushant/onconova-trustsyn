from pathlib import Path

import argparse
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error
from scipy.stats import pearsonr
from xgboost import XGBRegressor

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# -------------------------------------------------------
# Load datasets
# -------------------------------------------------------

# -------------------------------------------------------
# Command-line arguments
# -------------------------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument(
    "--split",
    default="random",
    choices=["random", "cold_drug", "cold_cell", "cold_pair"],
)

parser.add_argument("--version", default="baseline_v1")

args = parser.parse_args()

SPLIT = args.split
VERSION = args.version

TRAIN = PROJECT_ROOT / "splits" / SPLIT / "train.csv"
VALID = PROJECT_ROOT / "splits" / SPLIT / "valid.csv"

DRUG = PROJECT_ROOT / "data" / "lookup" / "drug_features_final.csv"

RESULTS_DIR = PROJECT_ROOT / "results" / VERSION / SPLIT

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

train = pd.read_csv(TRAIN)
valid = pd.read_csv(VALID)

drug = pd.read_csv(DRUG)

print("Train:", train.shape)
print("Valid:", valid.shape)
print("Drug :", drug.shape)

# -------------------------------------------------------
# Keep only fingerprint columns
# -------------------------------------------------------

fp_cols = [str(i) for i in range(2048)]

drug_fp = drug[["NSC"] + fp_cols].copy()

drug_fp[fp_cols] = drug_fp[fp_cols].astype("float32")

# -------------------------------------------------------
# Merge Drug A fingerprints
# -------------------------------------------------------

train = train.merge(drug_fp, left_on="drug_A", right_on="NSC", how="left")
train.drop(columns=["NSC"], inplace=True)
train.rename(columns={c: f"A_{c}" for c in fp_cols}, inplace=True)

# ------------------------------------------------------------

train = train.merge(drug_fp, left_on="drug_B", right_on="NSC", how="left")
train.drop(columns=["NSC"], inplace=True)
train.rename(columns={c: f"B_{c}" for c in fp_cols}, inplace=True)

# -------------------------------------------------------
# Validation merges
# -------------------------------------------------------

valid = valid.merge(drug_fp, left_on="drug_A", right_on="NSC", how="left")
valid.drop(columns=["NSC"], inplace=True)
valid.rename(columns={c: f"A_{c}" for c in fp_cols}, inplace=True)

# ------------------------------------------------------------

valid = valid.merge(drug_fp, left_on="drug_B", right_on="NSC", how="left")
valid.drop(columns=["NSC"], inplace=True)
valid.rename(columns={c: f"B_{c}" for c in fp_cols}, inplace=True)

print("\nMerged")
print(train.shape)
print(valid.shape)

# -------------------------------------------------------
# Encode cell line
# -------------------------------------------------------

le = LabelEncoder()

all_cells = pd.concat([train["CELLNAME"], valid["CELLNAME"]])

le.fit(all_cells)

train["cell"] = le.transform(train["CELLNAME"])
valid["cell"] = le.transform(valid["CELLNAME"])

# -------------------------------------------------------
# Feature matrix
# -------------------------------------------------------

feature_cols = ["cell"] + [f"A_{i}" for i in fp_cols] + [f"B_{i}" for i in fp_cols]

X_train = train[feature_cols]

y_train = train["combo_score"]

X_valid = valid[feature_cols]

y_valid = valid["combo_score"]

print("\nTraining matrix:", X_train.shape)

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

print("\nTraining baseline...")

model.fit(X_train, y_train)

print("Done.")

# -------------------------------------------------------
# Prediction
# -------------------------------------------------------

pred = model.predict(X_valid)

print("\nSample predictions:\n")

comparison = pd.DataFrame({"Actual": y_valid.values[:10], "Predicted": pred[:10]})

print(comparison)

import numpy as np

mse = mean_squared_error(y_valid, pred)

rmse = np.sqrt(mse)

mae = mean_absolute_error(y_valid, pred)

corr = pearsonr(y_valid, pred)[0]

print("\n===============================")
print("BASELINE RESULTS")
print("===============================")

print("RMSE    :", rmse)
print("MAE     :", mae)
print("Pearson :", corr)

# -------------------------------------------------------
# Save predictions
# -------------------------------------------------------

pred_df = pd.DataFrame({"Actual": y_valid.values, "Predicted": pred})

pred_path = RESULTS_DIR / "predictions.csv"

pred_df.to_csv(pred_path, index=False)

print(f"\nPredictions saved to:\n{pred_path}")

metrics_df = pd.DataFrame(
    {"Metric": ["RMSE", "MAE", "Pearson"], "Value": [rmse, mae, corr]}
)

metrics_path = RESULTS_DIR / "metrics.csv"

metrics_df.to_csv(metrics_path, index=False)

print(f"Metrics saved to:\n{metrics_path}")


MODEL_DIR = PROJECT_ROOT / "models" / VERSION

MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_DIR.mkdir(exist_ok=True)

joblib.dump(model, MODEL_DIR / f"{SPLIT}.pkl")

print("\nModel saved.")
