# TrustSyn Experiment Log

**Project:** TrustSyn - Drug Combination Synergy Prediction

This document records every major preprocessing step, dataset version, model experiment, and performance result. All future experiments should be appended to this log in chronological order.

---

# Experiment 001

## Date

03-Aug-2026

## Version

Baseline v1

## Status

Completed

---

## Objective

Establish a reproducible baseline model using molecular fingerprints before integrating CellMiner multi-omics features.

---

## Dataset

| Item | Value |
|------|------|
| Dataset | trustsyn_master.csv |
| Samples | 299,823 |
| Canonical Drugs | 104 |
| Cell Lines | 59 |

---

## Drug Features

- Morgan Fingerprints
- Radius = 2
- 2048 bits

---

## Cell Features

- Label encoded cell line only

No RNA, CNV, Mutation or Protein data included.

---

## Model

XGBoost Regressor

---

## Data Splits

Implemented

- Random
- Cold Drug
- Cold Cell
- Cold Pair

---

## Results

| Split | RMSE | MAE | Pearson |
|------|------:|------:|------:|
| Random | 5.712 | 3.882 | 0.609 |
| Cold Cell | 5.239 | 3.681 | 0.576 |
| Cold Pair | 6.799 | 4.406 | 0.324 |
| Cold Drug | 8.746 | 5.904 | 0.060 |

---

## Observations

- Random split produced the strongest performance.
- Cold Cell performance remained close to Random, indicating reasonable generalization across unseen cell lines.
- Cold Pair was more challenging because the model had not seen the specific drug combinations during training.
- Cold Drug was the most difficult benchmark, demonstrating that molecular fingerprints alone are insufficient for predicting synergy for completely unseen drugs.

---

## Major Pipeline Decisions

- Curated master dataset frozen as `trustsyn_master.csv`.
- Drug universe standardized to 104 canonical drugs.
- Cell line universe standardized to 59 CellMiner-compatible cell lines.
- Added NSC identifiers back into `drug_features_final.csv`.
- Created `drug_id_mapping.csv` to preserve mapping between internal drug IDs and NSC identifiers.
- Implemented four reproducible benchmark split strategies.
- Unified training into a single baseline script supporting multiple split types.

---

## Issues Encountered

### Drug identifier mismatch

Problem

The master dataset stored NSC identifiers while the drug feature table stored internal sequential IDs (1–104), resulting in failed merges and invalid cold-drug splits.

Resolution

- Created `drug_id_mapping.csv`.
- Restored NSC identifiers to `drug_features_final.csv`.
- Updated all merge operations to use NSC identifiers.

Status

Resolved.

---

### Memory allocation error

Problem

Pandas attempted to allocate more than 6 GB of memory during chained `rename().drop()` operations after merging fingerprint features.

Resolution

- Replaced chained operations with `inplace=True`.
- Optimized merge workflow.
- Converted fingerprint matrix to `float32`.

Status

Resolved.

---

## Lessons Learned

- Validate every preprocessing step before building models.
- Preserve original identifiers throughout the pipeline.
- Benchmark using multiple evaluation strategies instead of relying solely on a random split.
- Fix root-cause data issues rather than introducing downstream workarounds.
- Keep preprocessing, lookup tables, modeling datasets, and benchmark results clearly separated.

---

## Next Experiment

Experiment 002

Objective

Integrate RNA expression features into the baseline model and evaluate performance on all four benchmark splits.

Status

Planned.

---

# Revision History

| Version | Date | Description |
|---------|------|-------------|
| Baseline v1 | 03-Aug-2026 | Initial benchmark framework established with four evaluation protocols and XGBoost baseline. |