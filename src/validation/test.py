import pandas as pd

master = pd.read_csv("data/processed/master/trustsyn_master.csv")
drug = pd.read_csv("data/lookup/drug_features_final.csv")

print("Master drug_A range:")
print(master["drug_A"].min(), master["drug_A"].max())

print()

print("Lookup drug_id range:")
print(drug["drug_id"].min(), drug["drug_id"].max())

print()

print("First 10 master drug IDs:")
print(master["drug_A"].unique()[:10])

print()

print("First 10 lookup drug IDs:")
print(drug["drug_id"].unique()[:10])
