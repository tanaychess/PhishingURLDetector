# An Explainable Machine Learning Framework for Phishing Website Detection Using URL-Based Features

**Author**: Tanay Samson Pathare  
**Affiliation**: Department of Computer Science, Bhonsala Military College, Nashik, Maharashtra, India  
**Email**: tanaypathare1@gmail.com  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

---

## 1. Executive Summary & Research Motivation

Phishing attacks represent one of the most persistent and damaging attack vectors in modern cybersecurity, causing billions of dollars in annual identity theft and financial fraud. While traditional security infrastructures rely heavily on blacklist lookups (e.g., Google Safe Browsing, PhishTank), blacklists suffer from a 2- to 48-hour discovery latency window during which newly deployed zero-hour phishing domains achieve maximum victim exploitation.

Machine learning (ML) classifiers enable automated detection of unseen URLs. However, typical deployments face two critical roadblocks:
1. **The "Black-Box" Trust Barrier**: High accuracy without interpretability prevents Security Operations Center (SOC) analysts and end-users from validating predictions or understanding false alarms.
2. **Exploit Risks & Latency of Dynamic Crawling**: Systems requiring full web-page crawling, DOM parsing, or JavaScript rendering expose client-side scanners to drive-by malware payloads and introduce prohibitive network traversal latencies (500ms–2s per URL).

This repository contains the complete, reproducible research codebase and IEEE-format conference manuscript.

---

## 2. Research Questions (RQs)

- **RQ1 (Model Superiority)**: Which machine-learning architecture (Logistic Regression, Decision Tree, Random Forest, Linear SVM, or XGBoost) provides the highest discriminative performance across Accuracy, F1-Score, and ROC-AUC on static URL features?
- **RQ2 (Attribution & Explainability)**: Which URL-based lexical and structural features contribute most decisively to phishing predictions under game-theoretic SHAP attributions?
- **RQ3 (Feature Reduction Viability)**: Can an ultra-compact subset of top SHAP features (e.g., Top-20 or Top-10) maintain competitive classification performance while cutting computational latency?
- **RQ4 (Computational Efficiency)**: What are the computational runtime, memory footprints, and inference latency trade-offs between full and reduced feature sets?
- **RQ5 (Local Interpretability)**: How effectively can local TreeSHAP explanations assist human triage by converting numeric risk scores into actionable URL component attributions?

---

## 3. Dataset Provenance & Sentinel Handling

- **Primary Dataset**: Vrbančič et al. (2020), published in *Data in Brief* (Elsevier, [DOI: 10.1016/j.dib.2020.106438](https://doi.org/10.1016/j.dib.2020.106438)).
- **Sample Count**: **58,645 total URLs** (30,647 Phishing [52.26%], 27,998 Legitimate [47.74%]).
- **Feature Space**: 111 structured static metrics spanning URL Lexical (20), Domain Structural (21 raw -> 8 non-zero), Directory/Path (18), File-Level (18), Query Parameter (20), and External Resolver Lookups (14). Total retained features: **98 non-zero features** (84 static lexical + 14 resolver/network).
- **Partitioning**: 80% Stratified Training Set (46,916 samples) / 20% Held-Out Test Set (11,729 samples: 6,129 phishing, 5,600 legitimate).
- **Sentinel Encoding Disclosure**: Features such as `directory_length`, `time_domain_activation`, and sub-delimiters utilize a -1 sentinel value to denote "not applicable" (e.g., domain without directory path, unresolvable/masked WHOIS record, or lookup timeout). In error analyses, medians and conditional distributions are evaluated on valid subsets to avoid -1 bias.
- **Data Leakage Guarantee**: All transformers, scalers, variance selectors, and TreeSHAP explainer structures are fitted strictly on the training partition.

---

## 4. Key Experimental Results & Statistical Rigor

All numerical results are verified and mathematically validated on the 11,729 held-out test partition:

### A. Multi-Model Benchmark Comparison (Full 98 Features)
### A. Multi-Model Benchmark Comparison (Full 98 Features, Table III)
| Model Architecture | Accuracy (%) | Precision (%) | Recall (%) | F1-Score (%) | ROC-AUC | PR-AUC | 5-Fold CV F1 (%) | Latency (ms/1k) | Model Size |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGBoost (Champion)** | **94.82%** | **94.88%** | **95.22%** | **95.05%** | **0.9879** | **0.9889** | **95.17% ± 0.13%** | **2.46 ± 0.20 ms** | **0.126 MB** |
| Random Forest | 94.30% | 94.03% | 95.12% | 94.57% | 0.9867 | 0.9878 | 94.79% ± 0.11% | 10.60 ± 0.31 ms | 4.068 MB |
| Decision Tree | 93.61% | 93.36% | 94.49% | 93.92% | 0.9668 | 0.9575 | 93.62% ± 0.17% | 0.53 ± 0.05 ms | 0.029 MB |
| Linear SVM (Platt Calibrated) | 89.99% | 89.10% | 92.12% | 90.58% | 0.9613 | 0.9637 | 90.45% ± 0.22% | 2.85 ± 0.20 ms | 0.006 MB |
| Logistic Regression | 89.97% | 89.23% | 91.91% | 90.55% | 0.9613 | 0.9637 | 90.48% ± 0.20% | 1.41 ± 0.16 ms | 0.004 MB |

*Note on Linear Models*: Logistic Regression and Linear SVM converge to identical decision rankings under L2 regularization on standardized features. Their weight vectors have cosine similarity $0.8307$ and their test decision scores have Spearman rank correlation $\rho_s = 0.9997$ ($r = 0.9836$), rendering their ROC-AUC (0.9613) and PR-AUC (0.9637) indistinguishable at 4 decimal places.

### B. Statistical Significance & Stability
- **McNemar's Paired Test**: Comparing XGBoost vs. Random Forest on the 11,729 test samples yields $b=161$ (XGBoost correct, RF incorrect) vs. $c=100$ (RF correct, XGBoost incorrect), giving $\chi^2 = 13.79$ ($p = 2.04 \times 10^{-4} < 0.001$), confirming statistically significant superiority.
- **Multi-Seed Variance (5 seeds: 42, 123, 456, 789, 2024)**: XGBoost F1 is $94.98\% \pm 0.08\%$ vs. RF $94.59\% \pm 0.06\%$.
- **Train-Only Attribution & Ranking Stability**: When retraining the underlying model across 5 seeds, rank agreement remains robust ($\rho_s = 0.973 \pm 0.010$ across all 98 features, Kendall's $\tau = 0.795$ within Top-20, and 95.0% top-20 set overlap). When varying explanation subsamples on a fixed model, $\rho_s = 0.9991$ across 98 features and Kendall's $\tau = 0.9131$ within the Top-20.

### C. Feature Reduction & Computational Trade-Offs (Table V)
| Configuration | Features (Net/Lex) | Accuracy (%) | F1-Score (%) | ROC-AUC | Inference (ms/1k) | Model Size (MB) | Throughput (q/s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| XGBoost (Full 98) | 14N / 84L | 94.82% | 95.05% | 0.9879 | 2.46 ± 0.20 ms | 0.126 MB | 406,318 |
| XGBoost (Top-30) | 12N / 18L | 94.74% | 94.97% | 0.9882 | 1.83 ± 0.07 ms | 0.134 MB | 546,448 |
| **XGBoost (Top-20, Smallest within 0.2 pp)** | **11N / 9L** | **94.82%** | **95.05%** | **0.9876** | **1.67 ± 0.06 ms** | **0.130 MB** | **600,099** |
| XGBoost (Top-10) | 5N / 5L | 94.19% | 94.48% | 0.9859 | 1.57 ± 0.11 ms | 0.126 MB | 636,942 |
| XGBoost (Top-5) | 1N / 4L | 91.32% | 91.84% | 0.9723 | 1.59 ± 0.12 ms | 0.121 MB | 628,930 |
| **XGBoost (Lexical-84, Zero Net)** | **0N / 84L** | **89.68%** | **90.04%** | **0.9627** | **3.16 ± 0.43 ms** | **0.342 MB** | **316,002** |

*Key Findings*:
1. **$k=20$ Selection**: Selected via 5-fold CV on training data as the smallest subset within about 0.2 pp of full performance ($95.02\%$ at $k=20$, $95.17\%$ at $k=30$, $95.20\%$ at $k=98$). Note: SHAP rankings were computed on all of D_train, so CV scores for top-k are slightly optimistic, while test results remain unaffected. Multi-seed test mean across 5 seeds: $94.71\% \pm 0.09\%$ Accuracy, $94.95\% \pm 0.08\%$ F1-score.
2. **Two-Tier Uncertainty-Gated Cascade**:
   - Tier 1 (Lexical-84, threshold band $[0.10, 0.90]$) autonomously resolves **64.28%** of URLs (7,539 / 11,729) in-memory with **97.78%** accuracy, eliminating resolver lookups for nearly two-thirds of traffic.
   - Tier 1 test leakage rate is $2.66\%$ ($90$ phishing leaks / 3,380 URLs called legitimate), slightly above the $2.5\%$ CV design target.
   - Conditional Tier-1 phishing recall is $97.84\%$ ($4,082 / 4,172$) on resolved URLs. Accounting for deferred URLs, the **end-to-end cascade** achieves Accuracy $94.57\%$, F1 $94.81\%$, FNR $4.98\%$, and FPR $5.93\%$ (vs. Monolithic Full XGBoost: Acc $94.82\%$, F1 $95.05\%$, FNR $4.78\%$, FPR $5.62\%$).
   - Root-domain blind spot: $88$ of $141$ pathless phishing test URLs ($62.4\%$) are predicted legitimate at Tier 1, highlighting an operational limitation against root-domain phishing.
   - Path-bearing vs. Pathless URLs: On the 8,212 path-bearing test URLs, full XGBoost achieves $93.59\%$ accuracy and $95.64\%$ F1 (vs. naive path heuristic $72.92\%$). On the 3,517 pathless URLs, monolithic XGBoost catches only 47.5% of pathless phishing (67/141; Recall = 47.52%, F1 = 62.04%), and its $97.67\%$ pathless accuracy stands merely 1.7 pp above the naive all-legitimate baseline of 96.0% (3,376/3,517).

---

## 5. Directory Structure

```text
PhishingURLDetetctor/
├── README.md                          # Comprehensive project documentation
├── requirements.txt                   # Locked Python package dependencies
├── LICENSE                            # Open-source MIT License
├── .gitignore                         # Standard git ignore rules
│
├── config/
│   └── config.yaml                    # Master experiment configuration & hyperparameters
│
├── data/
│   ├── raw/
│   │   └── dataset_small.csv          # Verified 58,645 URL benchmark dataset
│   ├── processed/
│   │   ├── train.csv                  # 80% Stratified training set (46,916 rows)
│   │   └── test.csv                   # 20% Held-out test set (11,729 rows)
│   └── README.md                      # Dataset provenance & schema documentation
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py                 # Dataset loader and stratified train/test split
│   ├── preprocessing.py               # Leakage-free variance filtering and z-score scaling
│   ├── feature_engineering.py         # URL security feature taxonomy & descriptions
│   ├── models.py                      # Factory for LR, DT, RF, SVM, and XGBoost models
│   ├── train.py                       # 5-fold CV and test evaluation orchestrator
│   ├── evaluate.py                    # Metric calculator (Acc, Prec, Rec, F1, ROC, PR, Latency)
│   ├── explainability.py              # TreeSHAP explainer, global rankings & local plots
│   ├── feature_selection.py           # Dimensionality reduction benchmarking (Full to Top-5)
│   ├── resource_measurement.py        # Profiling of model storage, memory, and throughput
│   ├── export_latex.py                # Automated export of CSV results to LaTeX tables
│   ├── validate_results.py            # Scientific mathematical consistency validator
│   ├── generate_paper_figures.py      # High-resolution publication figures generator
│   ├── generate_manuscript_pdf.py     # High-fidelity IEEE two-column PDF compiler
│   └── predict_url.py                 # Live interactive URL prediction & explainability CLI
│
├── experiments/
│   ├── run_all.py                     # Master end-to-end experiment pipeline (Single command)
│   ├── run_baseline.py                # Baseline 5-model benchmarking script
│   ├── run_explainability.py          # SHAP global and local attribution script
│   └── run_feature_selection.py       # Dimensionality reduction experiment script
│
├── results/
│   ├── metrics/                       # Validated CSV metric outputs
│   │   ├── model_comparison.csv
│   │   ├── feature_selection_results.csv
│   │   └── computational_benchmarks.csv
│   ├── predictions/
│   │   └── test_predictions.csv       # Test set predicted labels and continuous probabilities
│   └── explanations/
│   │   ├── shap_global_feature_importance.csv
│   │   └── local_explanations.csv
│
├── figures/                           # 10 High-resolution publication figures (300 DPI PNG & PDF)
│   ├── fig1_system_architecture.pdf
│   ├── fig2_class_distribution.pdf
│   ├── fig3_model_comparison.pdf
│   ├── fig4_confusion_matrices.pdf
│   ├── fig5_roc_pr_curves.pdf
│   ├── fig6_shap_feature_importance.pdf
│   ├── fig7_shap_summary_beeswarm.pdf
│   ├── fig8_local_shap_explanation.pdf
│   ├── fig9_feature_reduction_comparison.pdf
│   └── fig10_computational_comparison.pdf
│
├── notebooks/                         # Interactive Jupyter notebooks for step-by-step exploration
│   ├── 01_data_exploration.ipynb
│   ├── 02_baseline_models.ipynb
│   ├── 03_explainability.ipynb
│   └── 04_feature_selection.ipynb
│
├── paper/
│   ├── overleaf/                      # Complete Overleaf-ready LaTeX package
│   │   ├── main.tex                   # Master IEEE document (Author: Tanay Samson Pathare)
│   │   ├── references.bib             # Verified BibTeX citations with real DOIs
│   │   ├── IEEEtran.cls               # Official IEEEtran conference document class
│   │   ├── README.md                  # Overleaf import instructions
│   │   ├── sections/                  # Modular .tex sections
│   │   ├── tables/                    # Automated LaTeX tables
│   │   ├── figures/                   # Vector PDF & PNG figures
│   │   └── PhishingURLDetetctor_Overleaf.zip
│   └── final/
│       └── PhishingURLDetetctor.pdf   # Final compiled manuscript
│
└── docs/
    ├── research_plan.md               # Formal research design and objectives
    ├── experiment_plan.md             # Detailed experimental execution protocols
    ├── literature_matrix.csv          # Comprehensive 15-paper literature review matrix
    ├── viva_questions.md              # 30 Comprehensive defense Q&As
    ├── presentation_outline.md        # 12-Slide presentation outline & speaker notes
    └── reviewer_checklist.md          # Strict simulated academic peer review audit
```

---

## 6. Installation & Execution Guide

### Step 1: Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Reproduce Tables and Manuscript Artifacts
You can reproduce specific tables or the entire experiment suite with individual commands:

- **Reproduce Table III (Multi-Model Comparison, N=11,729)**:
  ```bash
  python experiments/run_baseline.py
  ```
  *Outputs*: `results/metrics/model_comparison.csv`, `paper/overleaf/tables/tab3_model_comparison.tex`

- **Reproduce Table V (Feature Reduction & Latency Benchmarks)**:
  ```bash
  python experiments/run_feature_selection.py
  ```
  *Outputs*: `results/metrics/feature_selection_results.csv`, `paper/overleaf/tables/tab5_feature_selection.tex`

- **Run Full Master Pipeline (All Experiments, Explanations & Plots)**:
  ```bash
  python experiments/run_all.py
  ```

- **Validate Numerical Consistency & Mathematical Integrity**:
  ```bash
  python src/validate_results.py
  ```

- **Compile Publication IEEE 4-Page PDF**:
  ```bash
  python src/generate_manuscript_pdf.py
  ```
  *Outputs*: `paper/final/PhishingURLDetetctor.pdf` and refreshed `paper/overleaf/PhishingURLDetetctor_Overleaf.zip`

### Step 3: Interactive Live URL Prediction & Explanation
```bash
python src/predict_url.py --sample 5
```

---

## 7. Overleaf & Paper Compilation

1. Locate the pre-packaged archive: `paper/PhishingURLDetetctor_Overleaf.zip`.
2. Navigate to [Overleaf](https://www.overleaf.com/) and click **New Project** -> **Upload Project**.
3. Upload `PhishingURLDetetctor_Overleaf.zip`.
4. Compile with standard **pdfLaTeX**.

---

## 8. Double-Blind Review & Anonymization Guidelines

For venues requiring **double-blind peer review**, prepare the submission copy by applying these anonymization steps:
1. **Author & Affiliation**: In `paper/overleaf/main.tex` (lines 35–42), replace author names and institutional affiliations with `\author{\IEEEauthorblockN{Anonymous Authors}\IEEEauthorblockA{\textit{Anonymous Institution / Department}\\Email: anonymous@institution.org}}`.
2. **Repository URL**: In `paper/overleaf/sections/conclusion.tex` (or the Data & Code Availability section), mask the GitHub URL to: `https://anonymous.4open.science/r/PhishingURLDetetctor` (or an anonymous GitHub mirror).
3. **Acknowledgment**: Comment out `\section*{Acknowledgment}` in `paper/overleaf/main.tex` and `sections/conclusion.tex` during initial submission.
4. For **single-blind** or **camera-ready** submission, retain the author and affiliation details as currently populated.

---

## 9. Author Contact

**Tanay Samson Pathare**  
Department of Computer Science, Bhonsala Military College  
Nashik, Maharashtra, India  
Email: [tanaypathare1@gmail.com](mailto:tanaypathare1@gmail.com)

