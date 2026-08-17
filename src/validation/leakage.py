import pandas as pd

train = pd.read_csv("splits/cold_drug/train.csv")
valid = pd.read_csv("splits/cold_drug/valid.csv")
test = pd.read_csv("splits/cold_drug/test.csv")

train_drugs = set(train["drug_A"]) | set(train["drug_B"])
valid_drugs = set(valid["drug_A"]) | set(valid["drug_B"])
test_drugs = set(test["drug_A"]) | set(test["drug_B"])

print("Train drugs:", len(train_drugs))
print("Valid drugs:", len(valid_drugs))
print("Test drugs :", len(test_drugs))

print("Train ∩ Valid:", len(train_drugs & valid_drugs))
print("Train ∩ Test :", len(train_drugs & test_drugs))
print("Valid ∩ Test :", len(valid_drugs & test_drugs))
