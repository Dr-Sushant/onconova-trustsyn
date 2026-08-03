from pathlib import Path
import json

import numpy as np
import pandas as pd

# ============================================================
# Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MASTER_DATA = PROJECT_ROOT / "data" / "source" / "nci_almanac_with_cellminer_ids.csv"

DRUG_LOOKUP = PROJECT_ROOT / "data" / "lookup" / "drug_features_final.csv"

OUTPUT_DIR = PROJECT_ROOT / "splits" / "cold_drug"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42

# ============================================================
# Load data
# ============================================================

print("=" * 60)
print("LOADING DATA")
print("=" * 60)

df = pd.read_csv(MASTER_DATA)

drug_features = pd.read_csv(DRUG_LOOKUP)

print(f"Master dataset : {df.shape}")
print(f"Drug features  : {drug_features.shape}")

# ============================================================
# Canonical drug list
# ============================================================

canonical_drugs = sorted(drug_features["NSC"].unique())

print(f"\nCanonical drugs : {len(canonical_drugs)}")

# ============================================================
# Shuffle drugs
# ============================================================

rng = np.random.default_rng(SEED)

canonical_drugs = np.array(canonical_drugs)

rng.shuffle(canonical_drugs)

n = len(canonical_drugs)

n_train = int(0.70 * n)
n_valid = int(0.15 * n)
n_test = n - n_train - n_valid

train_drugs = set(canonical_drugs[:n_train])
valid_drugs = set(canonical_drugs[n_train : n_train + n_valid])
test_drugs = set(canonical_drugs[n_train + n_valid :])

print("\nDrug split")
print("----------------------------")
print("Train :", len(train_drugs))
print("Valid :", len(valid_drugs))
print("Test  :", len(test_drugs))

# ============================================================
# Assign rows
# ============================================================


def assign_split(row):

    a = row["drug_A"]
    b = row["drug_B"]

    if a in train_drugs and b in train_drugs:
        return "train"

    if a in valid_drugs and b in valid_drugs:
        return "valid"

    if a in test_drugs and b in test_drugs:
        return "test"

    return "discard"


df["split"] = df.apply(assign_split, axis=1)

train = df[df["split"] == "train"].drop(columns="split")
valid = df[df["split"] == "valid"].drop(columns="split")
test = df[df["split"] == "test"].drop(columns="split")

discarded = df[df["split"] == "discard"]

# ============================================================
# Leakage checks
# ============================================================

print("\nChecking leakage...")

train_used = set(train["drug_A"]).union(train["drug_B"])
valid_used = set(valid["drug_A"]).union(valid["drug_B"])
test_used = set(test["drug_A"]).union(test["drug_B"])

assert len(train_used & valid_used) == 0
assert len(train_used & test_used) == 0
assert len(valid_used & test_used) == 0

print("Leakage check passed.")

# ============================================================
# Save CSVs
# ============================================================

train.to_csv(OUTPUT_DIR / "train.csv", index=False)
valid.to_csv(OUTPUT_DIR / "valid.csv", index=False)
test.to_csv(OUTPUT_DIR / "test.csv", index=False)

# ============================================================
# Metadata
# ============================================================

metadata = {
    "split_type": "cold_drug",
    "seed": SEED,
    "master_dataset": "nci_almanac_with_cellminer_ids.csv",
    "drug_lookup": "drug_features_final.csv",
    "total_drugs": int(len(canonical_drugs)),
    "total_cell_lines": int(df["CELLNAME"].nunique()),
    "train_drugs": int(len(train_drugs)),
    "valid_drugs": int(len(valid_drugs)),
    "test_drugs": int(len(test_drugs)),
    "train_rows": int(len(train)),
    "valid_rows": int(len(valid)),
    "test_rows": int(len(test)),
    "discarded_rows": int(len(discarded)),
}

with open(OUTPUT_DIR / "metadata.json", "w") as f:

    json.dump(metadata, f, indent=4)

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("COLD DRUG SPLIT COMPLETE")
print("=" * 60)

print(f"Train rows    : {len(train):,}")
print(f"Valid rows    : {len(valid):,}")
print(f"Test rows     : {len(test):,}")
print(f"Discarded     : {len(discarded):,}")

print("\nFiles written")

print(OUTPUT_DIR / "train.csv")
print(OUTPUT_DIR / "valid.csv")
print(OUTPUT_DIR / "test.csv")
print(OUTPUT_DIR / "metadata.json")
