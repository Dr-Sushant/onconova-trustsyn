from pathlib import Path
import pandas as pd

# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUR_FILE = PROJECT_ROOT / "data" / "processed" / "split_dataset.csv"

TEAM_FILE = PROJECT_ROOT / "data" / "source" / "nci_almanac_with_cellminer_ids.csv"

# ==========================================================
# Load datasets
# ==========================================================

print("=" * 70)
print("LOADING DATASETS")
print("=" * 70)

our_df = pd.read_csv(OUR_FILE)
team_df = pd.read_csv(TEAM_FILE)

print(f"Our dataset : {our_df.shape}")
print(f"Team dataset: {team_df.shape}")

# ==========================================================
# Row count
# ==========================================================

print("\n" + "=" * 70)
print("ROW COUNT")
print("=" * 70)

print("Our rows :", len(our_df))
print("Team rows:", len(team_df))

if len(our_df) == len(team_df):
    print("PASS: Row counts match")
else:
    print("FAIL: Row counts differ")

# ==========================================================
# Unique drugs
# ==========================================================

print("\n" + "=" * 70)
print("UNIQUE DRUGS")
print("=" * 70)

our_drugs = set(our_df["drug_1_id"]) | set(our_df["drug_2_id"])

team_drugs = set(team_df["drug_A"]) | set(team_df["drug_B"])

print("Our unique drugs :", len(our_drugs))
print("Team unique drugs:", len(team_drugs))

print("Drug sets identical:", our_drugs == team_drugs)

# ==========================================================
# Unique cell lines
# ==========================================================

print("\n" + "=" * 70)
print("CELL LINES")
print("=" * 70)

our_cells = set(our_df["cell_line"])
team_cells = set(team_df["CELLNAME"])

print("Our cell lines :", len(our_cells))
print("Team cell lines:", len(team_cells))

print("Cell sets identical:", our_cells == team_cells)

# ==========================================================
# Drug pairs
# ==========================================================

print("\n" + "=" * 70)
print("DRUG PAIRS")
print("=" * 70)

our_pairs = set(zip(our_df["drug_1_id"], our_df["drug_2_id"]))

team_pairs = set(zip(team_df["drug_A"], team_df["drug_B"]))

print("Our drug pairs :", len(our_pairs))
print("Team drug pairs:", len(team_pairs))

print("Drug pair sets identical:", our_pairs == team_pairs)

# ==========================================================
# Experiment Keys
# ==========================================================

print("\n" + "=" * 70)
print("EXPERIMENT KEYS")
print("=" * 70)

our_keys = set(zip(our_df["drug_1_id"], our_df["drug_2_id"], our_df["cell_line"]))

team_keys = set(zip(team_df["drug_A"], team_df["drug_B"], team_df["CELLNAME"]))

print("Our experiment keys :", len(our_keys))
print("Team experiment keys:", len(team_keys))

print("Experiment keys identical:", our_keys == team_keys)

# ==========================================================
# Missing Experiments
# ==========================================================

print("\n" + "=" * 70)
print("MISSING EXPERIMENTS")
print("=" * 70)

only_ours = our_keys - team_keys
only_team = team_keys - our_keys

print("Only in our dataset :", len(only_ours))
print("Only in team dataset:", len(only_team))

# ==========================================================
# Compare combo scores
# ==========================================================

print("\n" + "=" * 70)
print("COMPARING COMBO SCORES")
print("=" * 70)

our_compare = our_df[
    [
        "drug_1_id",
        "drug_2_id",
        "cell_line",
        "combo_score",
    ]
].copy()

our_compare.columns = [
    "drug_A",
    "drug_B",
    "CELLNAME",
    "our_score",
]

team_compare = team_df[
    [
        "drug_A",
        "drug_B",
        "CELLNAME",
        "combo_score",
    ]
].copy()

team_compare.columns = [
    "drug_A",
    "drug_B",
    "CELLNAME",
    "team_score",
]

merged = our_compare.merge(
    team_compare,
    on=["drug_A", "drug_B", "CELLNAME"],
    how="inner",
)

print("Matched experiments:", len(merged))

merged["difference"] = (merged["our_score"] - merged["team_score"]).abs()

mismatch = merged[merged["difference"] > 1e-6]

print("Score mismatches:", len(mismatch))

# ==========================================================
# Save mismatch report
# ==========================================================

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

REPORT_FILE = REPORT_DIR / "dataset_difference_report.csv"

mismatch.to_csv(REPORT_FILE, index=False)

print("\nReport saved to:")
print(REPORT_FILE)

print("\nComparison complete.")
