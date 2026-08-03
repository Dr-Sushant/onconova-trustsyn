from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FILE = PROJECT_ROOT / "data" / "lookup" / "drug_features_final_old.csv"

df = pd.read_csv(FILE)

print("=" * 60)
print("DRUG FEATURES AUDIT")
print("=" * 60)

print(f"\nShape: {df.shape}")

print("\nColumns:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nDuplicate drug_id:", df["drug_id"].duplicated().sum())
print("Duplicate Drug_Name:", df["Drug_Name"].duplicated().sum())

print("\nFirst 10 rows:")
print(df[["drug_id", "Drug_Name"]].head(10))

print("\nLast 10 rows:")
print(df[["drug_id", "Drug_Name"]].tail(10))
