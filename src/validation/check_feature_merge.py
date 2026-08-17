from pathlib import Path
import argparse
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

parser = argparse.ArgumentParser()

parser.add_argument("--feature_table", required=True)

args = parser.parse_args()

MASTER = PROJECT_ROOT / "data" / "processed" / "master" / "trustsyn_master.csv"
FEATURE = PROJECT_ROOT / "data" / "features" / args.feature_table

master = pd.read_csv(MASTER)
feature = pd.read_csv(FEATURE)

print("\nMASTER UNIQUE DRUGS")
print("----------------------")

master_drugs = set(master["drug_A"]).union(set(master["drug_B"]))

feature_drugs = set(feature["NSC"])

print("Unique drugs in master :", len(master_drugs))
print("Unique drugs in feature:", len(feature_drugs))

missing = master_drugs - feature_drugs

print("Missing drugs:", len(missing))

if len(missing):

    print("\nFirst missing IDs")

    print(sorted(list(missing))[:20])

else:

    print("\n✓ 100% drug coverage")

print("=" * 60)
print("MASTER")
print("=" * 60)
print(master.shape)

print("\nFEATURE TABLE")
print("=" * 60)
print(feature.shape)

print("\nColumns")
print(feature.columns.tolist())

print(sorted(missing))
