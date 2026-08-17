# OncoNova - TrustSyn

## Predicting Anti-Cancer Drug Combination Activity

**Team:** OncoNova  
**System:** TrustSyn  
**Challenge:** Novartis Discoverathon 2026 - Challenge 1: Predicting Drug Combination Activity

---

## 1. Overview

TrustSyn is the computational drug-combination prediction system developed by **OncoNova** for the Novartis Discoverathon 2026 Challenge 1.

The project is centered on the **NCI-ALMANAC** drug-combination screening dataset and integrates molecular and cell-line information to investigate prediction of anti-cancer drug combination activity.

Over the course of development, the team built and evaluated a multi-stage computational pipeline covering:

- NCI-ALMANAC data curation and quality control
- Drug and cell-line identification and canonicalization
- CellMiner molecular feature integration
- Drug structural and molecular feature construction
- Additional biological feature sources, including STRING and KEGG-derived features
- Multiple train/validation/test evaluation regimes
- Classical machine-learning baselines
- Deep molecular representation learning
- Ensemble and stacking experiments
- Model comparison and robustness analysis
- Uncertainty and trust-oriented analysis
- Explainability analysis
- Final model and evaluation artifact consolidation

The repository documents the computational work performed by **OncoNova** and provides a reproducible structure for inspecting the project.

<img width="1620" height="810" alt="final_stack_rmse" src="https://github.com/user-attachments/assets/0c5ffe18-18b6-4fcb-845c-c973c246f0a7" />

---

# 2. Central Data Foundation

## NCI-ALMANAC

The central experimental response dataset for TrustSyn is the **NCI-ALMANAC** drug-combination screening resource.

The original source data are processed through the repository's preprocessing pipeline to separate single-drug and combination experiments and construct modeling-ready datasets.

The primary data lineage is:

NCI-ALMANAC
    |
    v
ComboDrugGrowth_Nov2017.csv
    |
    v
01_load_dataset.py
    |
    +-- single_drug.csv
    |
    +-- combination_drug.csv
            |
            v
05_prepare_split_dataset.py
            |
            v
      modeling-ready data
            |
            v
      feature integration
            |
            v
        benchmarks
            |
            v
       TrustSyn models

3. Data Curation and Feature Engineering

The development pipeline includes drug and cell-line curation before model training.

Drug-related processing

The repository contains workflows for:

canonical drug identification
NSC/drug mapping
alias mapping
drug-pair canonicalization
structural representation
molecular fingerprints
target-related features
drug similarity
additional drug-pair biological features
Cell-line and molecular features

CellMiner-derived information was integrated for compatible NCI-60 cell lines.

Feature development includes molecular information derived from:

RNA expression
copy-number / CNV information
mutation information
protein information
drug structure
molecular fingerprints
target information
drug similarity
STRING-derived drug-pair features
KEGG-derived drug-pair features

The exact feature set varies by experiment and benchmark. The repository therefore distinguishes the broader feature-engineering work from any individual final model configuration.

4. Benchmark Evaluation

TrustSyn was developed and evaluated using multiple evaluation regimes designed to measure both standard predictive performance and generalization.

Benchmark	Purpose
RANDOM	Standard random/IID-style evaluation
COLD_COMBINATION	Evaluation involving unseen drug combinations
COLD_CELL_LINE	Generalization to unseen cell lines
COLD_DRUG	Generalization to unseen drugs

The cold evaluations are intended to examine model behavior under distribution shift rather than relying exclusively on random holdout performance.

The repository contains split-generation and validation code for these evaluation regimes.

| Setting          | Selected model     |  RMSE |    R² |
| ---------------- | ------------------ | ----: | ----: |
| RANDOM           | Ridge meta-model   | 5.888 | 0.294 |
| COLD_COMBINATION | XGBoost meta-model | 6.568 | 0.129 |
| COLD_CELL_LINE   | XGBoost meta-model | 6.789 | 0.323 |
| COLD_DRUG        | Stacked model      | 4.858 | 0.351 |

<img width="1620" height="810" alt="ranking" src="https://github.com/user-attachments/assets/a1b7ce57-558d-4da3-8fe1-c1e019c89ea7" />

5. Models Investigated

The OncoNova development process evaluated multiple model families rather than relying on a single algorithm.

Deep molecular model
D-MPNN

A Directed Message Passing Neural Network was developed for molecular representation learning, including the TrustSyn D-MPNN V2-C development lineage.

The final D-MPNN lineage includes trained checkpoints, training/evaluation artifacts, and model documentation within the final model package.

Classical machine-learning benchmarks

The project also investigated:

XGBoost
LightGBM
CatBoost
Ridge regression / stacking components

These models provide comparative benchmarks and, where applicable, contribute to ensemble experiments.

The repository does not treat every model investigated during development as an independent final TrustSyn system. Instead, the model families are documented according to their role in the development and ensemble lineage.

6. Ensemble and Stacking

TrustSyn development included ensemble experiments combining predictions from multiple model families.

The final model lineage contains dedicated artifacts for:

base-model results
stacking tables
meta-model predictions
ensemble results
final frozen evaluation results

The complete final lineage is retained in the local:

final_model/Complete_model

package.

This package contains the consolidated final-model evidence across the D-MPNN, CatBoost, stacking, trust-layer, and explainability components.

The public GitHub repository is intentionally kept smaller than this complete local audit package.

7. Evaluation Metrics

The project evaluates both numerical prediction quality and ranking behavior.

Regression metrics
MAE
RMSE
Pearson correlation
Spearman correlation
Ranking metrics

Where applicable, the benchmark includes:

Precision@50
Precision@100
Recall@100
nDCG@100
Enrichment@100
Additional analyses
generalization gaps
data-efficiency analysis
baseline comparisons
robustness comparisons
model agreement
uncertainty analysis

Reported metrics should always be interpreted together with their corresponding evaluation regime.

8. Trust Layer

A major objective of the TrustSyn development was to move beyond a single predicted score and investigate whether predictions can be accompanied by information about their reliability.

The final model lineage contains work covering:

ensemble uncertainty
conformal prediction
novelty assessment
final trust scoring
calibration / reliability-oriented analysis
explainability

The objective is not to imply that a prediction is clinically validated.

Instead, the trust layer is intended to help identify predictions that may require greater scrutiny because of uncertainty, novelty, or limited similarity to the model's observed training domain.

<img width="1620" height="756" alt="coverage" src="https://github.com/user-attachments/assets/4800b544-1202-4f60-ae0e-c66796f03170" />

9. Explainability

The final model package contains explainability artifacts for the major evaluation regimes, including SHAP-based analyses.

These analyses are intended to help inspect:

feature contributions
model behavior
differences between evaluation settings
potential sources of prediction variation

Explainability outputs are treated as model-analysis tools rather than proof of biological mechanism.

<img width="1620" height="900" alt="shap_top10" src="https://github.com/user-attachments/assets/a116d1c5-c27a-4106-a703-e21ed6d83562" />

10. Repository Structure

The repository is organized around the development and reproducibility workflow:

OncoNova / TrustSyn
|
+-- data/
|   +-- raw/
|   +-- source/
|   +-- lookup/
|   +-- processed/
|   +-- features/
|
+-- src/
|   +-- preprocessing/
|   +-- splits/
|   +-- models/
|   +-- validation/
|   +-- utils/
|   +-- experiments/
|
+-- results/
|   +-- final/
|
+-- reports/
|
+-- notebooks/
|
+-- configs/
|
+-- checkpoints/
|
+-- docs/
|
+-- extra/
    +-- COMPLETE_MODEL_AUDIT/
        +-- Complete_model/

The final_model/Complete_model package is retained as the local consolidated final-model lineage and evidence archive.

11. Reproducibility

The repository contains source code for the major stages of the computational workflow, including:

Dataset loading
Data exploration
Drug and cell-line extraction
Dataset preparation
Drug feature integration
Drug mapping and preprocessing
Benchmark split generation
Model training
Feature-based baselines
Benchmark evaluation
Feature validation
Leakage-oriented checks
Model comparison

Large source and intermediate datasets are not duplicated indiscriminately into the Git repository.

Instead, the repository preserves the code and documented data lineage required to understand how the modeling datasets were constructed.

12. Scientific Scope

TrustSyn is a computational research and prioritization system.

Its predictions are intended to support prioritization of candidate drug combinations for further experimental investigation.

Predictions do not establish:

biological mechanism
clinical efficacy
therapeutic safety
clinical benefit

Experimental and clinical validation remain necessary.

13. Scientific Integrity

The project distinguishes measured computational results from interpretation.

The evaluation framework is designed to expose:

performance across multiple benchmark regimes
behavior under distribution shift
baseline comparisons
ranking performance
data-efficiency behavior
robustness
uncertainty
novelty
model limitations

The strongest evaluation result should not be interpreted in isolation from weaker or more difficult generalization settings.

14. Final Model Lineage

The final consolidated TrustSyn evidence package contains the major components developed during the project:

NCI-ALMANAC
    |
    v
Data curation
    |
    v
Molecular / cell-line feature integration
    |
    v
Multiple predictive models
    |
    +-- D-MPNN
    +-- XGBoost
    +-- LightGBM
    +-- CatBoost
    +-- Ridge / stacking components
    |
    v
Ensemble / stacking analysis
    |
    v
Final TrustSyn results
    |
    +-- uncertainty
    +-- conformal prediction
    +-- novelty
    +-- trust scoring
    +-- explainability

The final consolidated artifacts are maintained under:

final_model/Complete_model

This separation allows the repository to remain practical while preserving the complete local model-development and final-evaluation lineage.

15. Limitations

Important limitations include:

NCI-ALMANAC is an experimental screening resource and does not directly represent clinical treatment outcomes.
Molecular feature availability differs across drugs and cell lines.
Cold-start benchmarks represent specific forms of distribution shift and do not encompass every possible deployment scenario.
Model performance can vary substantially across evaluation regimes.
Computational uncertainty does not equal biological or clinical uncertainty.
Novelty detection does not establish whether a novel prediction is biologically correct.
Model explanations should not be interpreted as causal biological mechanisms.
Final predictions require experimental validation before therapeutic conclusions can be drawn.
16. Team

OncoNova

System

TrustSyn

Challenge

Novartis Discoverathon 2026 - Challenge 1: Predicting Drug Combination Activity

17. AI Assistance Disclosure

ChatGPT (OpenAI) was used as an AI-assisted development and documentation tool during the project, including for code drafting and debugging support, data-analysis workflow assistance, technical writing, documentation, presentation development, and critical review of implementation logic.

The team remained responsible for:

scientific reasoning
methodological decisions
model development
data preparation
evaluation
interpretation of results
verification of reported outputs
final submission decisions

AI-generated suggestions were reviewed against project artifacts before inclusion.

OncoNova

TrustSyn - computational prediction and trust-oriented analysis of anti-cancer drug combination activity.
