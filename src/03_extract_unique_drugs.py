import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_ROOT / "data" / "processed" / "combination_drug.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "unique_drugs.csv"

# Load combination dataset
df = pd.read_csv(DATA_FILE, low_memory=False)

# Extract unique NSC IDs from both columns
drug_ids = sorted(set(df["NSC1"]).union(set(df["NSC2"])))

# Create lookup table
drug_df = pd.DataFrame({"NSC": drug_ids})

# Save
drug_df.to_csv(OUTPUT_FILE, index=False)

print(f"Unique drugs: {len(drug_df)}")
print(drug_df.head(10))

print(f"\nSaved to:\n{OUTPUT_FILE}")

unique_drugs = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "unique_drugs.csv")

print(unique_drugs.head(20))
print(unique_drugs.columns.tolist())
