from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FILE = PROJECT_ROOT / "data" / "processed" / "combination_drug.csv"

df = pd.read_csv(FILE, nrows=5)

print("=" * 60)
print("COMBINATION DRUG DATASET")
print("=" * 60)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())
