from pathlib import Path

import pandas as pd

# ==========================================================
# Project paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FEATURES = PROJECT_ROOT / "data" / "lookup" / "drug_features_final.csv"

MAPPING = PROJECT_ROOT / "data" / "lookup" / "drug_id_mapping.csv"

BACKUP = PROJECT_ROOT / "data" / "lookup" / "drug_features_final_backup.csv"

# ==========================================================
# Load files
# ==========================================================

print("=" * 60)
print("LOADING FILES")
print("=" * 60)

features = pd.read_csv(FEATURES)
mapping = pd.read_csv(MAPPING)

print("Features :", features.shape)
print("Mapping  :", mapping.shape)

# ==========================================================
# Backup original
# ==========================================================

features.to_csv(BACKUP, index=False)

print("\nBackup created:")
print(BACKUP)

# ==========================================================
# Merge NSC information
# ==========================================================

updated = mapping.merge(features, on=["drug_id", "Drug_Name"], how="inner")

# ==========================================================
# Reorder columns
# ==========================================================

fixed_columns = [
    "drug_id",
    "NSC",
    "Drug_Name",
    "canonical_smiles",
    "InChIKey",
    "targets",
]

embedding_columns = [c for c in updated.columns if c not in fixed_columns]

embedding_columns = [c for c in embedding_columns if c != "drug_id"]

updated = updated[fixed_columns + embedding_columns]

# ==========================================================
# Save
# ==========================================================

updated.to_csv(FEATURES, index=False)

print("\nUpdated file saved:")
print(FEATURES)

print("\nShape:", updated.shape)

print("\nColumns:")

print(updated.columns[:10].tolist())

print("...")

print(updated.columns[-10:].tolist())

print("\nDone.")
