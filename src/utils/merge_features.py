import pandas as pd


def merge_drug_features(train, valid, feature_df):
    """
    Merge drug-level features for Drug A and Drug B.
    """

    feature_cols = [
        c
        for c in feature_df.columns
        if c
        not in [
            "NSC",
            "Drug_Name",
            "drug_id",
            "canonical_smiles",
            "InChIKey",
            "targets",
            "ChEMBL_ID",
        ]
    ]

    drug_fp = feature_df[["NSC"] + feature_cols].copy()

    drug_fp[feature_cols] = drug_fp[feature_cols].astype("float32")

    # ----------------------------
    # Train
    # ----------------------------

    train = train.merge(
        drug_fp,
        left_on="drug_A",
        right_on="NSC",
        how="left",
    )

    train.drop(columns="NSC", inplace=True)

    train.rename(
        columns={c: f"A_{c}" for c in feature_cols},
        inplace=True,
    )

    train = train.merge(
        drug_fp,
        left_on="drug_B",
        right_on="NSC",
        how="left",
    )

    train.drop(columns="NSC", inplace=True)

    train.rename(
        columns={c: f"B_{c}" for c in feature_cols},
        inplace=True,
    )

    # ----------------------------
    # Valid
    # ----------------------------

    valid = valid.merge(
        drug_fp,
        left_on="drug_A",
        right_on="NSC",
        how="left",
    )

    valid.drop(columns="NSC", inplace=True)

    valid.rename(
        columns={c: f"A_{c}" for c in feature_cols},
        inplace=True,
    )

    valid = valid.merge(
        drug_fp,
        left_on="drug_B",
        right_on="NSC",
        how="left",
    )

    valid.drop(columns="NSC", inplace=True)

    valid.rename(
        columns={c: f"B_{c}" for c in feature_cols},
        inplace=True,
    )

    feature_cols = [f"A_{c}" for c in feature_cols] + [f"B_{c}" for c in feature_cols]

    return train, valid, feature_cols


def merge_cell_features(train, valid, feature_df):
    """
    Merge CellMiner feature tables (RNA, Protein, Mutation, CNV)
    using CELLNAME.
    """

    feature_cols = [c for c in feature_df.columns if c != "CELLNAME"]

    feature_df[feature_cols] = feature_df[feature_cols].astype("float32")

    train = train.merge(
        feature_df,
        on="CELLNAME",
        how="left",
    )

    valid = valid.merge(
        feature_df,
        on="CELLNAME",
        how="left",
    )

    return train, valid, feature_cols


def merge_pair_features(train, valid, feature_df):
    """
    Merge pairwise features using
    drug_A + drug_B + CELLNAME
    """

    key_cols = ["drug_A", "drug_B", "CELLNAME"]

    feature_cols = [c for c in feature_df.columns if c not in key_cols]

    train = train.merge(
        feature_df,
        on=key_cols,
        how="left",
    )

    valid = valid.merge(
        feature_df,
        on=key_cols,
        how="left",
    )

    return train, valid, feature_cols
