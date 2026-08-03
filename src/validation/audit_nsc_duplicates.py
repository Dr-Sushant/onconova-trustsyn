from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FILE = PROJECT_ROOT / "data" / "processed" / "split_dataset.csv"

df = pd.read_csv(FILE, usecols=["drug_1_id", "drug_1_name", "drug_2_id", "drug_2_name"])

print(df.columns.tolist())
print()
print(df.head())

drug1 = df[["drug_1_id", "drug_1_name"]].rename(
    columns={"drug_1_id": "NSC", "drug_1_name": "Drug_Name"}
)

drug2 = df[["drug_2_id", "drug_2_name"]].rename(
    columns={"drug_2_id": "NSC", "drug_2_name": "Drug_Name"}
)

drugs = pd.concat([drug1, drug2], ignore_index=True).drop_duplicates()

print(f"Unique NSCs      : {drugs['NSC'].nunique()}")
print(f"Unique Drug Names: {drugs['Drug_Name'].nunique()}")

duplicates = drugs.groupby("Drug_Name")["NSC"].apply(list).reset_index()

duplicates = duplicates[duplicates["NSC"].apply(len) > 1]

print("\nDrug names with multiple NSCs:\n")
print(duplicates)
