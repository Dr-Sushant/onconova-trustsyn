from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

canon = pd.read_csv(PROJECT_ROOT / "data" / "lookup" / "canonical_drug_table.csv")

alias = pd.read_csv(PROJECT_ROOT / "data" / "lookup" / "nsc_drug_alias_mapping.csv")

print("=" * 60)
print("ALIAS MAPPING VALIDATION")
print("=" * 60)

print("\nAlias table:")
print(alias)

print("\nCanonical entry for drug_id = 101:")
print(canon.loc[canon["drug_id"] == 101, ["NSC", "Drug_Name", "drug_id"]])

print("\nCanonical table shape:", canon.shape)
print("Alias table shape:", alias.shape)
