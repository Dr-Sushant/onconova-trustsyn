from pathlib import Path
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SPLIT_FILE = PROJECT_ROOT / "data" / "processed" / "split_dataset.csv"

DRUG_FILE = PROJECT_ROOT / "data" / "lookup" / "drug_features_final_old.csv"

OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "master" / "master_with_drugs.csv"

CANONICAL_FILE = PROJECT_ROOT / "data" / "lookup" / "canonical_drug_table.csv"

ALIAS_FILE = PROJECT_ROOT / "data" / "lookup" / "nsc_drug_alias_mapping.csv"

# --------------------------------------------------
# Load datasets
# --------------------------------------------------

print("Loading split dataset...")
split_df = pd.read_csv(SPLIT_FILE)

print("Loading drug feature dataset...")
drug_df = pd.read_csv(DRUG_FILE)

print("Loading canonical drug table...")
canon_df = pd.read_csv(CANONICAL_FILE)

print("Loading alias table...")
alias_df = pd.read_csv(ALIAS_FILE)

print("\nDatasets loaded successfully.\n")

print(f"Split dataset shape : {split_df.shape}")
print(f"Drug dataset shape  : {drug_df.shape}")

print("\nSplit dataset columns:")
print(split_df.columns.tolist())

print("\nDrug dataset columns:")
print(drug_df.columns.tolist())

print("\nChecking drug IDs...")

print("\nUnique Drug IDs in split dataset (drug_1):", split_df["drug_1_id"].nunique())

print("Unique Drug IDs in split dataset (drug_2):", split_df["drug_2_id"].nunique())

print("Unique Drug IDs in drug feature table:", drug_df["drug_id"].nunique())

print("\nDuplicate drug IDs in lookup table:", drug_df["drug_id"].duplicated().sum())

print("\nChecking NSC mapping...")

# NSCs present in ALMANAC
split_nscs = set(split_df["drug_1_id"].astype(int)) | set(
    split_df["drug_2_id"].dropna().astype(int)
)

# Canonical NSCs
canonical_nscs = set(canon_df["NSC"].astype(int))

# Alias NSCs (duplicates like 753082)
alias_nscs = set(alias_df["NSC"].astype(int))

# Every NSC that can be resolved
available_nscs = canonical_nscs | alias_nscs

missing = split_nscs - available_nscs

print(f"Unique NSCs in split dataset : {len(split_nscs)}")
print(f"Canonical NSCs              : {len(canonical_nscs)}")
print(f"Alias NSCs                  : {len(alias_nscs)}")
print(f"Resolvable NSCs             : {len(available_nscs)}")
print(f"Missing NSCs                : {len(missing)}")

if missing:
    print(sorted(missing))

print("\nColumn dtypes:")
print(f"drug_1_id dtype : {split_df['drug_1_id'].dtype}")
print(f"drug_2_id dtype : {split_df['drug_2_id'].dtype}")
print(f"drug_id dtype   : {drug_df['drug_id'].dtype}")

print("\nSample values:")

print("drug_1_id:")
print(split_df["drug_1_id"].head().tolist())

print("\ndrug_id:")
print(drug_df["drug_id"].head().tolist())

print(drug_df.iloc[:10, :5])

print(drug_df[["drug_id", "Drug_Name"]].head(20))


print(f"Canonical table shape : {canon_df.shape}")
print(f"Alias table shape     : {alias_df.shape}")

# ==================================================
# Build lookup dictionaries
# ==================================================

print("\nBuilding lookup dictionaries...")

# Direct mapping: NSC -> drug_id
canonical_map = dict(zip(canon_df["NSC"], canon_df["drug_id"]))

# Alias mapping: duplicate NSC -> canonical drug_id
alias_map = dict(zip(alias_df["NSC"], alias_df["drug_id"]))

print(f"Canonical mappings : {len(canonical_map)}")
print(f"Alias mappings     : {len(alias_map)}")

print("\nTesting first 10 drug_1 mappings...")

for nsc in split_df["drug_1_id"].head(10):

    if nsc in alias_map:
        drug_id = alias_map[nsc]
        source = "Alias"

    else:
        drug_id = canonical_map.get(nsc)
        source = "Canonical"

    print(f"NSC {nsc} --> Drug ID {drug_id} ({source})")

# ==================================================
# Map drug_1_id -> canonical drug_id
# ==================================================

print("\nMapping drug_1 IDs...")

split_df["drug_1_canonical_id"] = split_df["drug_1_id"].map(alias_map)

mask = split_df["drug_1_canonical_id"].isna()

split_df.loc[mask, "drug_1_canonical_id"] = split_df.loc[mask, "drug_1_id"].map(
    canonical_map
)

print("Missing drug_1 mappings:", split_df["drug_1_canonical_id"].isna().sum())

# ==================================================
# Map drug_2_id -> canonical drug_id
# ==================================================

print("\nMapping drug_2 IDs...")

split_df["drug_2_canonical_id"] = split_df["drug_2_id"].map(alias_map)

mask = split_df["drug_2_canonical_id"].isna()

split_df.loc[mask, "drug_2_canonical_id"] = split_df.loc[mask, "drug_2_id"].map(
    canonical_map
)

print("Missing drug_2 mappings:", split_df["drug_2_canonical_id"].isna().sum())

print("\nMapped dataset preview:")

print(
    split_df[
        [
            "drug_1_id",
            "drug_1_canonical_id",
            "drug_2_id",
            "drug_2_canonical_id",
        ]
    ].head(10)
)

# ==================================================
# Keep only drug features
# ==================================================

drug_features = drug_df.drop(
    columns=["Drug_Name", "canonical_smiles", "InChIKey", "targets"]
)

# ==================================================
# Prepare Drug Feature Lookup
# ==================================================

print("\nPreparing drug feature lookup...")

drug_features = drug_df.drop(
    columns=["Drug_Name", "canonical_smiles", "InChIKey", "targets"]
)

drug_features = drug_features.set_index("drug_id")

print("Drug feature table shape:")
print(drug_features.shape)

print(f"Fingerprint columns : {len(drug_features.columns)}")

# ==================================================
# Map Drug 1 fingerprints
# ==================================================

print("\nAdding Drug 1 fingerprints...")

for i, col in enumerate(drug_features.columns):

    split_df[f"drug1_fp_{col}"] = split_df["drug_1_canonical_id"].map(
        drug_features[col]
    )

    if (i + 1) % 100 == 0:
        print(f"{i+1}/{len(drug_features.columns)} columns completed")

print("Drug 1 fingerprints added.")
