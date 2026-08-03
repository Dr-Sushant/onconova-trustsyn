# TrustSyn Baseline v1 Report

**Project:** TrustSyn - Drug Combination Synergy Prediction

**Version:** Baseline v1

**Date:** 02-Aug-2026

---

# 1. Objective

Establish a reproducible baseline for predicting drug combination synergy on the NCI-ALMANAC dataset before incorporating CellMiner multi-omics features.

The baseline serves as the reference point against which all future feature engineering and model improvements will be evaluated.

---

# 2. Dataset

## Source

NCI-ALMANAC 2017 drug combination dataset

Final curated dataset:

```
data/processed/master/trustsyn_master.csv
```

### Dataset Summary

| Item | Count |
|------|-------|
| Total samples | 299,823 |
| Canonical drugs | 104 |
| Cell lines | 59 |
| Response | ComboScore |

---

# 3. Drug Representation

Drug fingerprints:

```
data/lookup/drug_features_final.csv
```

Representation:

- Morgan Fingerprints
- Radius = 2
- 2048 bits

Additional identifiers stored:

- Internal drug_id (1–104)
- NSC identifier
- Drug name
- Canonical SMILES

---

# 4. Cell Line Representation

Current baseline uses:

- Cell line categorical encoding (LabelEncoder)

No omics features are included in Baseline v1.

---

# 5. Cell Line Curation

Original NCI-60 contains 60 historical cell lines.

CellMiner omics datasets provide profiles for 59 usable cell lines.

Excluded:

- MDA-MB-468

Reason:

No CellMiner RNA, Protein, CNV or Mutation profile exists for this cell line.

The exclusion was intentional to ensure consistency across all omics modalities.

---

# 6. Data Splits

Four evaluation protocols were implemented.

---

## 6.1 Random Split

Purpose:

Standard machine learning benchmark.

Rows

Train: 209,876

Validation: 44,973

---

## 6.2 Cold Drug Split

Purpose:

Evaluate generalization to completely unseen drugs.

Properties

- No drug appears in multiple splits.

Rows

Train: 138,539

Validation: 5,859

Test: 7,724

Discarded rows:

147,701

---

## 6.3 Cold Cell Split

Purpose

Evaluate generalization to unseen cell lines.

Properties

- No cell line appears in multiple splits.

Rows

Train: 207,645

Validation: 41,034

Test: 51,144

---

## 6.4 Cold Pair Split

Purpose

Evaluate prediction on previously unseen drug combinations.

Properties

- No drug pair appears in multiple splits.

Unique drug pairs:

5,242

Rows

Train: 209,845

Validation: 45,017

Test: 44,961

---

# 7. Leakage Validation

All split strategies were validated.

Random

No restrictions.

Cold Drug

- No drug appears in both training and validation.
- No drug appears in both training and test.
- No drug appears in both validation and test.

Cold Cell

- No cell line appears in multiple splits.

Cold Pair

- No drug pair appears in multiple splits.

No leakage was detected.

---

# 8. Baseline Model

Model

XGBoost Regressor

Features

- Drug A fingerprint (2048 bits)
- Drug B fingerprint (2048 bits)
- Cell line encoding

Total input features

4097

Target

ComboScore

---

# 9. Baseline Results

| Split | RMSE | MAE | Pearson |
|------|------:|------:|------:|
| Random | 5.712 | 3.882 | 0.609 |
| Cold Cell | 5.239 | 3.681 | 0.576 |
| Cold Pair | 6.799 | 4.406 | 0.324 |
| Cold Drug | 8.746 | 5.904 | 0.060 |

---

# 10. Interpretation

Random split provides the highest performance because both drugs and cell lines are observed during training.

Cold Cell remains close to Random, indicating that drug fingerprints generalize reasonably well across unseen cell lines.

Cold Pair is more challenging because drug combinations are unseen although individual drugs are known.

Cold Drug is the most difficult benchmark because the model must predict synergy for completely unseen drugs.

Observed difficulty:

Random

↓

Cold Cell

↓

Cold Pair

↓

Cold Drug

This ordering is consistent with the expected difficulty of each evaluation protocol.

---

# 11. Project Structure

```
data/
    processed/
        master/
            trustsyn_master.csv

    lookup/
        drug_features_final.csv
        drug_id_mapping.csv
        canonical_drug_table.csv
        cellline_mapping.csv

splits/

    random/

    cold_drug/

    cold_cell/

    cold_pair/

models/

results/

reports/
```

---

# 12. Reproducibility

Random Seed

42

Fingerprint Size

2048

Cell Lines

59

Canonical Drugs

104

Dataset Version

TrustSyn Master v1

---

# 13. Next Phase

The following feature engineering experiments will be evaluated against Baseline v1.

1. RNA Expression

2. RNA + CNV

3. RNA + CNV + Mutation

4. RNA + CNV + Mutation + Protein

5. Feature selection and dimensionality reduction

6. Advanced machine learning and deep learning models

All future experiments must be compared against the Baseline v1 metrics reported above.

---

**Status:** Baseline v1 Complete