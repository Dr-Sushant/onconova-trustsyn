import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_ROOT / "data" / "processed" / "combination_drug.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "unique_cell_lines.csv"

# Load dataset
df = pd.read_csv(DATA_FILE, low_memory=False)

# Extract unique cell lines with tissue information
cell_df = (
    df[["CELLNAME", "PANEL"]]
    .drop_duplicates()
    .sort_values("CELLNAME")
    .reset_index(drop=True)
)

# Save
cell_df.to_csv(OUTPUT_FILE, index=False)

print(f"Unique cell lines: {len(cell_df)}")
print(cell_df.head(10))

print(f"\nSaved to:\n{OUTPUT_FILE}")
