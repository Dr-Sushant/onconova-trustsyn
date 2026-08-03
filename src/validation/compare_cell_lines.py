from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ORIGINAL = PROJECT_ROOT / "data" / "raw" / "ComboDrugGrowth_Nov2017.csv"
CURATED = PROJECT_ROOT / "data" / "source" / "nci_almanac_with_cellminer_ids.csv"

print("=" * 70)
print("LOADING DATASETS")
print("=" * 70)

orig = pd.read_csv(ORIGINAL, low_memory=False)
cur = pd.read_csv(CURATED)

print(f"Original rows : {len(orig):,}")
print(f"Curated rows  : {len(cur):,}")

print("\nExtracting unique cell lines...")

orig_cells = orig["CELLNAME"].astype(str).str.strip().sort_values().unique()

cur_cells = cur["CELLNAME"].astype(str).str.strip().sort_values().unique()

orig_set = set(orig_cells)
cur_set = set(cur_cells)

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"Original unique cell lines : {len(orig_set)}")
print(f"Curated unique cell lines  : {len(cur_set)}")

missing = sorted(orig_set - cur_set)
extra = sorted(cur_set - orig_set)

print("\nCell lines present in ORIGINAL but missing in CURATED:")
if len(missing) == 0:
    print("None")
else:
    for x in missing:
        print(" -", x)

print("\nCell lines present in CURATED but not ORIGINAL:")
if len(extra) == 0:
    print("None")
else:
    for x in extra:
        print(" -", x)

print("\n" + "=" * 70)
print("FULL ORIGINAL CELL LINE LIST")
print("=" * 70)

for c in sorted(orig_set):
    print(c)

print("\n" + "=" * 70)
print("FULL CURATED CELL LINE LIST")
print("=" * 70)

for c in sorted(cur_set):
    print(c)
