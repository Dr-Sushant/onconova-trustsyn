from pathlib import Path
import json
import pandas as pd
from sklearn.model_selection import train_test_split

# ==========================================================
# Configuration
# ==========================================================

RANDOM_SEED = 42

TRAIN_SIZE = 0.70
VALID_SIZE = 0.15
TEST_SIZE = 0.15

assert TRAIN_SIZE + VALID_SIZE + TEST_SIZE == 1.0

# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "source" / "nci_almanac_with_cellminer_ids.csv"

OUTPUT_DIR = PROJECT_ROOT / "splits" / "random"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# Load dataset
# ==========================================================

print("=" * 60)
print("LOADING CURATED ALMANAC DATASET")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)

print(f"Rows loaded : {len(df):,}")

# ==========================================================
# Random Split
# ==========================================================

print("\nCreating Train/Test split...")

train_df, temp_df = train_test_split(
    df,
    test_size=(VALID_SIZE + TEST_SIZE),
    random_state=RANDOM_SEED,
    shuffle=True,
)

print("Creating Validation/Test split...")

valid_df, test_df = train_test_split(
    temp_df,
    test_size=TEST_SIZE / (VALID_SIZE + TEST_SIZE),
    random_state=RANDOM_SEED,
    shuffle=True,
)

# ==========================================================
# Save CSVs
# ==========================================================

train_df.to_csv(OUTPUT_DIR / "train.csv", index=False)
valid_df.to_csv(OUTPUT_DIR / "valid.csv", index=False)
test_df.to_csv(OUTPUT_DIR / "test.csv", index=False)

# ==========================================================
# Metadata
# ==========================================================

metadata = {
    "source_dataset": str(INPUT_FILE.name),
    "random_seed": RANDOM_SEED,
    "train_rows": len(train_df),
    "valid_rows": len(valid_df),
    "test_rows": len(test_df),
    "total_rows": len(df),
    "train_fraction": TRAIN_SIZE,
    "valid_fraction": VALID_SIZE,
    "test_fraction": TEST_SIZE,
}

with open(OUTPUT_DIR / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)

# ==========================================================
# Summary
# ==========================================================

print("\n" + "=" * 60)
print("RANDOM SPLIT CREATED")
print("=" * 60)

print(f"Train : {len(train_df):,}")
print(f"Valid : {len(valid_df):,}")
print(f"Test  : {len(test_df):,}")

print("\nFiles written:")

print(OUTPUT_DIR / "train.csv")
print(OUTPUT_DIR / "valid.csv")
print(OUTPUT_DIR / "test.csv")
print(OUTPUT_DIR / "metadata.json")

print("\nDone.")

# ==========================================================
# Sanity Checks
# ==========================================================

assert len(train_df) + len(valid_df) + len(test_df) == len(df)

assert set(train_df.columns) == set(df.columns)
assert set(valid_df.columns) == set(df.columns)
assert set(test_df.columns) == set(df.columns)

print("\nSanity checks passed.")
