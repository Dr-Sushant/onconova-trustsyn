# TrustSyn Contribution Guide

## Branch Strategy

The `main` branch contains the official Baseline v1.

Do not modify the baseline directly.

Create a new branch for every experiment.

Examples

- feature/rna
- feature/protein
- feature/cnv
- feature/gnn

---

## Experiments

All new model development should be done inside:

src/experiments/

Each researcher should work inside their own folder.

Example:

src/experiments/sushant/

src/experiments/sahiti/

src/experiments/anoushka/

---

## Baseline

Do not edit:

- src/models/08_train_baseline.py

unless the whole team agrees.

---

## Reporting

Every completed experiment should be added to:

reports/experiment_log.md