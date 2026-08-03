from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

unique = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "unique_drugs.csv")
old = pd.read_csv(PROJECT_ROOT / "data" / "lookup" / "drug_features_final_old.csv")

print(f"Unique NSCs : {len(unique)}")
print(f"Drug table  : {len(old)}")

print("\nFirst 20 NSCs:")
print(unique["NSC"].head(20).tolist())

print("\nLast 20 NSCs:")
print(unique["NSC"].tail(20).tolist())
