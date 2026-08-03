from pathlib import Path
import pandas as pd

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "unique_drugs.csv"

OUTPUT_FILE = PROJECT_ROOT / "data" / "lookup" / "drug_features_final.csv"

print("=" * 60)
print("Building Drug Feature Table")
print("=" * 60)

print(f"\nReading: {INPUT_FILE}")

drug_df = pd.read_csv(INPUT_FILE)

# ==========================================================
# Clean NSC IDs
# ==========================================================

drug_df["NSC"] = drug_df["NSC"].astype(int)

print(f"\nLoaded {len(drug_df)} unique drugs")

print("\nData types:")
print(drug_df.dtypes)

print("\nFirst five drugs:")
print(drug_df.head())
