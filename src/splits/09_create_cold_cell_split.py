from pathlib import Path
import json

import numpy as np
import pandas as pd

# ============================================================
# Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MASTER_DATA = PROJECT_ROOT / "data" / "processed" / "master" / "trustsyn_master.csv"

OUTPUT_DIR = PROJECT_ROOT / "splits" / "cold_cell"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42

# ============================================================
# Load
# ============================================================

print("=" * 60)
print("LOADING MASTER DATASET")
print("=" * 60)

df = pd.read_csv(MASTER_DATA)

print(df.shape)

# ============================================================
# Cell lines
# ============================================================

cell_lines = sorted(df["CELLNAME"].unique())

print(f"\nUnique cell lines : {len(cell_lines)}")

rng = np.random.default_rng(SEED)

cell_lines = np.array(cell_lines)

rng.shuffle(cell_lines)

n = len(cell_lines)

n_train = int(0.70 * n)
n_valid = int(0.15 * n)
n_test = n - n_train - n_valid

train_cells = set(cell_lines[:n_train])
valid_cells = set(cell_lines[n_train : n_train + n_valid])
test_cells = set(cell_lines[n_train + n_valid :])

print("\nCell line split")
print("---------------------------")
print("Train :", len(train_cells))
print("Valid :", len(valid_cells))
print("Test  :", len(test_cells))

# ============================================================
# Split rows
# ============================================================

train = df[df["CELLNAME"].isin(train_cells)]
valid = df[df["CELLNAME"].isin(valid_cells)]
test = df[df["CELLNAME"].isin(test_cells)]

# ============================================================
# Leakage check
# ============================================================

assert len(set(train["CELLNAME"]) & set(valid["CELLNAME"])) == 0

assert len(set(train["CELLNAME"]) & set(test["CELLNAME"])) == 0

assert len(set(valid["CELLNAME"]) & set(test["CELLNAME"])) == 0

print("\nLeakage check passed.")

# ============================================================
# Save
# ============================================================

train.to_csv(OUTPUT_DIR / "train.csv", index=False)
valid.to_csv(OUTPUT_DIR / "valid.csv", index=False)
test.to_csv(OUTPUT_DIR / "test.csv", index=False)

metadata = {
    "split_type": "cold_cell",
    "seed": SEED,
    "total_cell_lines": int(len(cell_lines)),
    "train_cell_lines": int(len(train_cells)),
    "valid_cell_lines": int(len(valid_cells)),
    "test_cell_lines": int(len(test_cells)),
    "train_rows": int(len(train)),
    "valid_rows": int(len(valid)),
    "test_rows": int(len(test)),
}

with open(OUTPUT_DIR / "metadata.json", "w") as f:

    json.dump(metadata, f, indent=4)

print("\n" + "=" * 60)
print("COLD CELL SPLIT COMPLETE")
print("=" * 60)

print(f"Train rows : {len(train):,}")
print(f"Valid rows : {len(valid):,}")
print(f"Test rows  : {len(test):,}")

print("\nFiles written")

print(OUTPUT_DIR / "train.csv")
print(OUTPUT_DIR / "valid.csv")
print(OUTPUT_DIR / "test.csv")
print(OUTPUT_DIR / "metadata.json")
