import pandas as pd
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dataset path
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "ComboDrugGrowth_Nov2017.csv"

print("=" * 60)
print("Loading dataset...")
print(DATA_FILE)
print("=" * 60)

# Read CSV
df = pd.read_csv(DATA_FILE)

print("\nDataset loaded successfully!\n")

# Basic information
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")

print("\nColumn Names:")
for col in df.columns:
    print(f" - {col}")

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\n===== Dataset Summary =====")

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

print(f"\nUnique Drug 1 IDs : {df['NSC1'].nunique():,}")
print(f"Unique Drug 2 IDs : {df['NSC2'].nunique():,}")

# Count unique drugs across both columns
all_drugs = set(df["NSC1"].dropna()).union(set(df["NSC2"].dropna()))
print(f"Total Unique Drugs: {len(all_drugs):,}")

print(f"\nUnique Cell Lines : {df['CELLNAME'].nunique():,}")
print(f"Unique Cancer Types : {df['PANEL'].nunique():,}")

print("\nVALID values:")
print(df["VALID"].value_counts())

print("\nMissing values:")
print(df.isnull().sum())

print("\n===== Unique Cancer Panels =====")
print(sorted(df["PANEL"].unique()))

print("\n===== Rows with missing NSC2 =====")
print(df[df["NSC2"].isna()].head())

print("\n===== Rows with missing SCORE =====")
print(df[df["SCORE"].isna()].head())

# Show ALL columns when printing
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", None)

print("\n===== First 5 rows with missing NSC2 =====")
print(df[df["NSC2"].isna()].head().to_string(index=False))

single_drug = df["NSC2"].isna().sum()
combo_drug = df["NSC2"].notna().sum()

print("\n===== Experiment Types =====")
print(f"Single-drug experiments : {single_drug:,}")
print(f"Combination experiments : {combo_drug:,}")

# Create processed directory if it doesn't exist
processed_dir = PROJECT_ROOT / "data" / "processed"
processed_dir.mkdir(exist_ok=True)

# Split datasets
single_drug_df = df[df["NSC2"].isna()].copy()
combination_df = df[df["NSC2"].notna()].copy()

# Save them
single_drug_df.to_csv(processed_dir / "single_drug.csv", index=False)
combination_df.to_csv(processed_dir / "combination_drug.csv", index=False)

print("\nFiles saved successfully!")
print(f"Single-drug rows : {len(single_drug_df):,}")
print(f"Combination rows : {len(combination_df):,}")
