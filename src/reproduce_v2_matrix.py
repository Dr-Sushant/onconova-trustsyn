import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(r"D:\Novartis\onconova-trustsyn")

# ============================================================
# INPUTS
# ============================================================

MASTER_PATH = ROOT / "data" / "processed" / "master" / "trustsyn_master.csv"

STRING_PATH = ROOT / "data" / "features" / "drug_pair_string_features_final.csv"
KEGG_PATH = ROOT / "data" / "features" / "drug_pair_kegg_features_final.csv"

STRUCTURE_PATH = ROOT / "data" / "features" / "drug_structure_features.csv"
TARGET_PATH = ROOT / "data" / "features" / "drug_target_features.csv"

SIMILARITY_PATH = ROOT / "data" / "features" / "drug_similarity_matrix.csv"

# ============================================================
# LOAD MASTER
# ============================================================

print("=" * 70)
print("TRUSTSYN V2 MATRIX RECONSTRUCTION")
print("=" * 70)

master = pd.read_csv(MASTER_PATH)

print("MASTER:", master.shape)
print("MASTER columns:", master.columns.tolist())

# ============================================================
# MASTER PAIR KEY
# ============================================================

def make_pair_key(a, b):
    a = str(a)
    b = str(b)
    return "_".join(sorted([a, b]))

master["PAIR_KEY"] = [
    make_pair_key(a, b)
    for a, b in zip(master["drug_A"], master["drug_B"])
]

print("Unique MASTER pairs:", master["PAIR_KEY"].nunique())

assert master["PAIR_KEY"].nunique() == 5143

master_pairs = (
    master[
        ["drug_A", "drug_B", "PAIR_KEY"]
    ]
    .drop_duplicates("PAIR_KEY")
    .copy()
)

print("MASTER PAIR MATRIX:", master_pairs.shape)

# ============================================================
# LOAD RAW PAIR FEATURES
# ============================================================

string = pd.read_csv(STRING_PATH)
kegg = pd.read_csv(KEGG_PATH)

structure = pd.read_csv(STRUCTURE_PATH)
target = pd.read_csv(TARGET_PATH)

similarity = pd.read_csv(SIMILARITY_PATH)

print("\nRAW SHAPES")
print("STRING     :", string.shape)
print("KEGG       :", kegg.shape)
print("STRUCTURE  :", structure.shape)
print("TARGET     :", target.shape)
print("SIMILARITY :", similarity.shape)

# ============================================================
# STRING
# ============================================================

string["PAIR_KEY"] = [
    make_pair_key(a, b)
    for a, b in zip(string["drug_A"], string["drug_B"])
]

string_pair = (
    string[
        ["PAIR_KEY", "STRING_distance"]
    ]
    .drop_duplicates("PAIR_KEY")
)

# STRING availability = whether distance exists
string_pair["STRING_available"] = (
    string_pair["STRING_distance"].notna().astype(int)
)

string_pair = string_pair[
    ["PAIR_KEY", "STRING_distance", "STRING_available"]
]

# ============================================================
# KEGG
# ============================================================

kegg["PAIR_KEY"] = [
    make_pair_key(a, b)
    for a, b in zip(kegg["drug_A"], kegg["drug_B"])
]

kegg_pair = (
    kegg[
        ["PAIR_KEY", "KEGG_overlap"]
    ]
    .drop_duplicates("PAIR_KEY")
)

# ============================================================
# CHECK DRUG-LEVEL STRUCTURE TABLE
# ============================================================

print("\nSTRUCTURE COLUMNS:")
print(structure.columns.tolist())

print("\nTARGET COLUMNS:")
print(target.columns.tolist())

print("\nSIMILARITY COLUMNS:")
print(similarity.columns.tolist())

print("\nSTOPPING HERE BEFORE PAIR CONSTRUCTION.")

print("The raw tables loaded successfully.")
print("MASTER pairs:", len(master_pairs))