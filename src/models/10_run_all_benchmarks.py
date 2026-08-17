from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# -------------------------------------------------------
# Feature tables
# -------------------------------------------------------

FEATURES = [
    # Drug features
    ("drug_morgan_fingerprints.csv", "drug"),
    ("drug_structure_features.csv", "drug"),
    ("drug_target_features.csv", "drug"),
    # Pair features
    ("drug_pair_kegg_features_final.csv", "pair"),
    # Uncomment once regenerated
    # ("drug_pair_string_features_final.csv", "pair"),
]

# -------------------------------------------------------
# Splits
# -------------------------------------------------------

SPLITS = [
    "random",
    "cold_drug",
    "cold_cell",
    "cold_pair",
]

# -------------------------------------------------------

total = len(FEATURES) * len(SPLITS)
current = 1

print("=" * 70)
print("Running Benchmark Suite")
print("=" * 70)

for feature_table, feature_type in FEATURES:

    for split in SPLITS:

        print("\n" + "=" * 70)
        print(f"[{current}/{total}]")
        print("Feature :", feature_table)
        print("Type    :", feature_type)
        print("Split   :", split)
        print("=" * 70)

        cmd = [
            sys.executable,
            "-m",
            "src.models.09_train_feature_baseline",
            "--split",
            split,
            "--feature_table",
            feature_table,
            "--feature_type",
            feature_type,
        ]

        result = subprocess.run(cmd)

        if result.returncode != 0:

            print("\nFAILED")
            print(feature_table)
            print(split)

        else:

            print("\nSUCCESS")

        current += 1

print("\n")
print("=" * 70)
print("Benchmark Suite Finished")
print("=" * 70)
