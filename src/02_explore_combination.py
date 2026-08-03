import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "combination_drug.csv"

# Load data
df = pd.read_csv(DATA_FILE, low_memory=False)

print("=" * 60)
print("COMBINATION DATASET SUMMARY")
print("=" * 60)

print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")

print("\nUnique Drug 1 IDs :", df["NSC1"].nunique())
print("Unique Drug 2 IDs :", df["NSC2"].nunique())

all_drugs = set(df["NSC1"]).union(set(df["NSC2"]))
print("Total Unique Drugs:", len(all_drugs))

print("\nUnique Cell Lines :", df["CELLNAME"].nunique())
print("Unique Cancer Types :", df["PANEL"].nunique())

print("\nCancer Types:")
print(df["PANEL"].value_counts())

print("\nTop 10 Cell Lines:")
print(df["CELLNAME"].value_counts().head(10))
