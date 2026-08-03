from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

drug = pd.read_csv(PROJECT_ROOT / "data" / "lookup" / "drug_features_final_old.csv")

print(drug.shape)

print(drug.columns[:15].tolist())

print()

print(drug.columns[-10:].tolist())

print()

print(drug.dtypes.head(15))
