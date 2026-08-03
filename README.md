# TrustSyn

Clinical AI pipeline for predicting anti-cancer drug combination synergy.

Built for the **Novartis Discoverathon 2026 – Challenge 1**.

---

# Project Overview

TrustSyn is a machine learning benchmark for predicting drug combination synergy using the NCI-ALMANAC dataset integrated with CellMiner molecular features.

The repository provides:

- Curated dataset preprocessing
- Canonical drug mapping
- Molecular fingerprint generation
- Benchmark train/validation/test splits
- Baseline XGBoost model
- Reproducible evaluation pipeline

---

# Dataset

Source:

- NCI-ALMANAC
- CellMiner

Current dataset contains:

- 104 canonical drugs
- 59 CellMiner-compatible cell lines

---

# Benchmark Splits

The repository includes four benchmark evaluation settings.

| Split | Purpose |
|--------|---------|
| Random | Standard IID evaluation |
| Cold Drug | Unseen drugs |
| Cold Cell | Unseen cell lines |
| Cold Pair | Unseen drug combinations |

---

# Baseline Model

Baseline model:

- XGBoost Regressor

Evaluation metrics:

- RMSE
- MAE
- Pearson Correlation

Baseline results are available in:

```
results/baseline_v1/
```

---

# Repository Structure

```
data/
src/
splits/
results/
reports/
models/
configs/
```

---

# Running the Pipeline

### Preprocessing

```
python src/preprocessing/build_drug_features.py
```

### Generate Splits

```
python src/splits/07_create_random_split.py
python src/splits/08_create_cold_drug_split.py
python src/splits/09_create_cold_cell_split.py
python src/splits/10_create_cold_pair_split.py
```

### Train Baseline

```
python src/models/08_train_baseline.py --split random
```

---

# Team Workflow

The baseline implementation inside

```
src/models/
```

should remain unchanged.

New experiments should be implemented inside

```
src/experiments/
```

Each experiment should be developed in a separate branch and merged through Pull Requests.

---

# License

MIT License