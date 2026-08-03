from pathlib import Path
import json
import numpy as np
import pandas as pd

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MASTER = PROJECT_ROOT / "data" / "processed" / "master" / "trustsyn_master.csv"
OUT_DIR = PROJECT_ROOT / "splits" / "cold_pair"

OUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42

# ------------------------------------------------------------
# Load
# ------------------------------------------------------------

print("=" * 60)
print("LOADING MASTER DATASET")
print("=" * 60)

df = pd.read_csv(MASTER)

print(df.shape)

# ------------------------------------------------------------
# Canonicalize pair
# (A,B) == (B,A)
# ------------------------------------------------------------

pair_df = pd.DataFrame(
    {
        "d1": np.minimum(df["drug_A"], df["drug_B"]),
        "d2": np.maximum(df["drug_A"], df["drug_B"]),
    }
)

df["pair"] = (
    pair_df["d1"].astype(int).astype(str) + "_" + pair_df["d2"].astype(int).astype(str)
)

pairs = np.array(sorted(df["pair"].unique()))

print("\nUnique drug pairs :", len(pairs))

# ------------------------------------------------------------
# Shuffle
# ------------------------------------------------------------

rng = np.random.default_rng(RANDOM_STATE)
rng.shuffle(pairs)

n = len(pairs)

train_pairs = set(pairs[: int(0.70 * n)])
valid_pairs = set(pairs[int(0.70 * n) : int(0.85 * n)])
test_pairs = set(pairs[int(0.85 * n) :])

print("\nPair split")
print("----------------------------")
print("Train :", len(train_pairs))
print("Valid :", len(valid_pairs))
print("Test  :", len(test_pairs))

# ------------------------------------------------------------
# Create splits
# ------------------------------------------------------------

train = df[df["pair"].isin(train_pairs)].drop(columns="pair")
valid = df[df["pair"].isin(valid_pairs)].drop(columns="pair")
test = df[df["pair"].isin(test_pairs)].drop(columns="pair")

# ------------------------------------------------------------
# Leakage check
# ------------------------------------------------------------

train_set = train_pairs
valid_set = valid_pairs
test_set = test_pairs

assert len(train_set & valid_set) == 0
assert len(train_set & test_set) == 0
assert len(valid_set & test_set) == 0

print("\nLeakage check passed.")

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

train.to_csv(OUT_DIR / "train.csv", index=False)
valid.to_csv(OUT_DIR / "valid.csv", index=False)
test.to_csv(OUT_DIR / "test.csv", index=False)

metadata = {
    "split": "cold_pair",
    "master_rows": int(len(df)),
    "unique_pairs": int(len(pairs)),
    "train_pairs": int(len(train_pairs)),
    "valid_pairs": int(len(valid_pairs)),
    "test_pairs": int(len(test_pairs)),
    "train_rows": int(len(train)),
    "valid_rows": int(len(valid)),
    "test_rows": int(len(test)),
    "random_state": RANDOM_STATE,
}

with open(OUT_DIR / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)

print("\n" + "=" * 60)
print("COLD PAIR SPLIT COMPLETE")
print("=" * 60)

print(f"Train rows : {len(train):,}")
print(f"Valid rows : {len(valid):,}")
print(f"Test rows  : {len(test):,}")

print("\nFiles written")
print(OUT_DIR / "train.csv")
print(OUT_DIR / "valid.csv")
print(OUT_DIR / "test.csv")
print(OUT_DIR / "metadata.json")
