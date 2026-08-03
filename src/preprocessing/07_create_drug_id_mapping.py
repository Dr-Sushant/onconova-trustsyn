from pathlib import Path

import pandas as pd

# ==========================================================
# Project paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CANONICAL = PROJECT_ROOT / "data" / "lookup" / "canonical_drug_table.csv"

FEATURES = PROJECT_ROOT / "data" / "lookup" / "drug_features_final.csv"

OUTPUT = PROJECT_ROOT / "data" / "lookup" / "drug_id_mapping.csv"

# ==========================================================
# Load files
# ==========================================================

print("=" * 60)
print("LOADING FILES")
print("=" * 60)

canonical = pd.read_csv(CANONICAL)
features = pd.read_csv(FEATURES)

print("Canonical :", canonical.shape)
print("Features  :", features.shape)

# ==========================================================
# Basic validation
# ==========================================================

assert len(canonical) == len(features), "Number of drugs differs between files."

assert canonical["Drug_Name"].equals(
    features["Drug_Name"]
), "Drug ordering differs. Cannot create mapping safely."

# ==========================================================
# Build mapping
# ==========================================================

mapping = pd.DataFrame(
    {
        "drug_id": features["drug_id"],
        "NSC": canonical["NSC"],
        "Drug_Name": canonical["Drug_Name"],
    }
)

# ==========================================================
# Save
# ==========================================================

mapping.to_csv(OUTPUT, index=False)

print("\nSaved to:")
print(OUTPUT)

print("\nFirst rows:\n")
print(mapping.head())

print("\nTotal drugs :", len(mapping))
