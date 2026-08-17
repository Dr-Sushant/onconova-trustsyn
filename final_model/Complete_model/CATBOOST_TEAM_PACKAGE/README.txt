TRUSTSYN — CATBOOST MODEL PACKAGE
===================================

This folder contains the files required to inspect, reproduce,
evaluate, and compare the TrustSyn CatBoost baseline model.

01_Notebook
-----------
CatBoost notebooks used during model development.

02_Final_Model
--------------
Final CatBoost .cbm model files organized by split.

03_Evaluation
-------------
Final CatBoost evaluation workbooks and comparison files.

04_Predictions
--------------
Saved model predictions for the evaluation splits.

05_Metrics
----------
Metric/result CSV and JSON files.

06_Feature_Ablation
-------------------
Feature ablation experiments and results.

07_Hyperparameter_Sweeps
------------------------
Hyperparameter optimization / sweep results.

08_Training_Validation
----------------------
Training, validation, and generalization results.

09_Baseline_Comparison
----------------------
CatBoost vs other baseline model evaluation files.

10_Documentation
----------------
Additional documentation can be placed here.

IMPORTANT
----------
Original TrustSyn files were NOT moved or modified.
This is a duplicate package intended for team sharing.

Canonical TrustSyn evaluation splits:
- RANDOM
- COLD_COMBINATION
- COLD_CELL_LINE
- COLD_DRUG

Primary regression metrics:
- MAE
- RMSE
- Pearson
- Spearman

Ranking metrics:
- Precision@50
- Precision@100
- Recall@100
- nDCG@100
- Enrichment@100

Other evaluation:
- Data-efficiency
- Generalization gap
- Baseline comparison
- Robustness