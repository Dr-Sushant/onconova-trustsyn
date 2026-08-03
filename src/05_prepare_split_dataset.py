import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_ROOT / "data" / "processed" / "combination_drug.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "split_dataset.csv"

# Load dataset
df = pd.read_csv(DATA_FILE, low_memory=False)

split_df = df[
    [
        "COMBODRUGSEQ",
        "NSC1",
        "NSC2",
        "SAMPLE1",
        "SAMPLE2",
        "CELLNAME",
        "PANEL",
        "SCORE",
    ]
].copy()

split_df.columns = [
    "sample_id",
    "drug_1_id",
    "drug_2_id",
    "drug_1_name",
    "drug_2_name",
    "cell_line",
    "tissue",
    "combo_score",
]

print(df.shape)
print(df.columns.tolist())

print(split_df.head())
print(split_df.shape)

print("\nMissing values:")
print(split_df.isnull().sum())

# Remove rows with missing combo_score
split_df = split_df.dropna(subset=["combo_score"]).reset_index(drop=True)

print("\nAfter removing missing combo_score:")
print(split_df.shape)

print("\nRemaining missing values:")
print(split_df.isnull().sum())

print("\nChecking for duplicate rows...")

duplicate_count = split_df.duplicated().sum()

print(f"Duplicate rows: {duplicate_count}")

# Count rows where drug_1_id > drug_2_id

reversed_pairs = (split_df["drug_1_id"] > split_df["drug_2_id"]).sum()

print(f"\nRows where drug_1_id > drug_2_id: {reversed_pairs:,}")

# Create canonical drug pair identifier
split_df["drug_pair_id"] = split_df.apply(
    lambda row: tuple(sorted([int(row["drug_1_id"]), int(row["drug_2_id"])])), axis=1
)

print("\nExample drug_pair_id values:")
print(split_df[["drug_1_id", "drug_2_id", "drug_pair_id"]].head())

# Create canonical drug pair ID (vectorized)
drug_min = split_df[["drug_1_id", "drug_2_id"]].min(axis=1).astype(int)
drug_max = split_df[["drug_1_id", "drug_2_id"]].max(axis=1).astype(int)

split_df["drug_pair_id"] = drug_min.astype(str) + "_" + drug_max.astype(str)

split_df.to_csv(OUTPUT_FILE, index=False)

print(f"\nPrepared dataset saved to:\n{OUTPUT_FILE}")
print(f"Final shape: {split_df.shape}")
