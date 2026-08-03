from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FILE = PROJECT_ROOT / "data" / "source" / "nci_almanac_with_cellminer_ids.csv"

df = pd.read_csv(FILE)

print("=" * 60)
print("UNIQUE CELL LINES")
print("=" * 60)

cell_lines = sorted(df["CELLNAME"].dropna().unique())

print(f"Count: {len(cell_lines)}\n")

for c in cell_lines:
    print(c)
