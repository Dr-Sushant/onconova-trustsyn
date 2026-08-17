TRUSTSYN — D-MPNN V2-C
=======================

This package contains the D-MPNN V2-C model artifacts for TrustSyn.

Contents
--------

FINAL_EVALUATION/
    Final evaluation workbook containing:
    - MAE
    - RMSE
    - Pearson
    - Spearman
    - Precision@50
    - Precision@100
    - Recall@100
    - nDCG@100
    - Enrichment@100
    - Data-efficiency results
    - Generalization gaps
    - CatBoost / LightGBM baseline comparisons
    - Robustness comparisons
    - Test predictions

CHECKPOINTS/
    Saved D-MPNN model checkpoints for each canonical split.

PREDICTIONS/
    Final test predictions for:
    - RANDOM
    - COLD_COMBINATION
    - COLD_CELL_LINE
    - COLD_DRUG

METRICS/
    Training histories and model summaries.

DATA_EFFICIENCY/
    Data-efficiency experiments and CSV results.

CONFIG/
    Model configuration / hyperparameter files where available.

FINAL_MODEL/
    D-MPNN-related notebooks where available.

Important
---------
Original TrustSyn files were NOT modified.
This folder is a duplicate package created for team sharing.

Canonical D-MPNN model:
D-MPNN V2-C

Canonical evaluation workbook:
TrustSyn_DMPNN_V2C_Final_Evaluation.xlsx
