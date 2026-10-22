# An Explainable Machine Learning Framework for Phishing Website Detection Using URL-Based Features

**Author**: Tanay Pathare  
**Affiliation**: Department of Computer Science, Bhonsala Military College, Nashik, Maharashtra, India  
**Email**: [tanaypathare1@gmail.com](mailto:tanaypathare1@gmail.com)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Paper PDF](https://img.shields.io/badge/Paper-PDF%20Available-red.svg)](paper/PhishingURLDetector.pdf)

---

## 1. Project Overview & Research Motivation

Phishing attacks represent one of the most pervasive cyber-attack vectors globally, causing billions of dollars in identity theft, credential stuffing, and organizational breaches annually. Conventional security systems rely on centralized blacklist feeds (e.g., Google Safe Browsing, PhishTank). However, blacklists suffer from an unavoidable **2- to 48-hour discovery latency window**, during which newly launched zero-hour phishing campaigns achieve maximum victim exploitation before domain flagging occurs.

Machine learning (ML) models offer immediate proactive detection for unseen URLs. Nonetheless, two foundational obstacles hinder their operational security adoption:
1. **The "Black-Box" Interpretability Deficit**: High classification accuracy without local interpretability prevents Security Operations Center (SOC) incident responders and end-users from understanding *why* an alert fired, undermining operational trust.
2. **Exploitation Risks & Latencies of Dynamic Crawling**: Systems requiring full HTML DOM scraping, screenshot capture, or headless browser execution expose detection infrastructures to drive-by malware payloads and suffer network traversal latencies exceeding 500 ms to 2,000 ms per URL.

### Research Solution
This project introduces a transparent, explainable machine-learning framework using **static URL-based and resolver features**. Using game-theoretic **TreeSHAP** (SHapley Additive exPlanations), the framework delivers:
- **Champion Classification**: Extreme Gradient Boosting (XGBoost) achieving **94.82% Accuracy, 95.05% F1-Score, and 0.9879 ROC-AUC** across 11,729 held-out test URLs.
- **Dimensionality Reduction**: Demonstrating that an ultra-compact **Top-20 SHAP feature subset** matches the full 98-feature model's performance (94.82% Accuracy, 95.05% F1) while accelerating batch throughput to **600,000+ queries/second**.
- **Two-Tier Uncertainty-Gated Cascade**: Deploying a fast lexical tier (Tier 1, zero external lookups) that autonomously resolves **64.28% of incoming traffic with 97.78% accuracy**, invoking resolver lookups only on ambiguous edge cases ($0.10 \le \hat{p} \le 0.90$).
- **Local Triage Interpretability**: Generating sample-level force/waterfall attribution plots that pinpoint malicious URL components (e.g., abnormal directory depth, suspicious anchor tokens, unindexed domain status) for human-in-the-loop validation.

---

## 2. Research Paper & Publication Manuscript

The comprehensive research paper detailing this methodology, empirical findings, and operational security trade-offs is provided directly in the repository:

* **Manuscript Location**: [`paper/PhishingURLDetector.pdf`](paper/PhishingURLDetector.pdf)
* **Format**: Publication-ready single-column scientific manuscript compliant with standard journal/conference layout specifications (custom typography, running headers, footers with page numbering, inline tables, and embedded high-DPI figures).
* **Automated PDF Generator**: Built and reproducible via [`src/generate_manuscript_pdf.py`](src/generate_manuscript_pdf.py).

---

## 3. Directory Structure

The repository has been restructured and cleaned for optimal modularity, maintainability, and reproducibility:

```text
PhishingURLDetector/
├── README.md                          # Master project documentation, benchmarks & execution guide
├── requirements.txt                   # Locked Python package dependencies
├── LICENSE                            # MIT Open-Source License
├── .gitignore                         # Git exclusion rules
│
├── config/
│   └── config.yaml                    # Global pipeline configuration, random seeds, and hyperparameters
│
├── data/                              # Dataset partitions
│   ├── raw/
│   │   └── dataset_small.csv          # Benchmark dataset (58,645 URLs, Vrbančič et al.)
│   └── processed/
│       ├── train.csv                  # 80% Stratified training partition (46,916 rows)
│       └── test.csv                   # 20% Held-out test partition (11,729 rows)
│
├── paper/                             # Research publication manuscript
│   └── PhishingURLDetector.pdf        # Final compiled research paper PDF
│
├── figures/                           # High-resolution vector PDF and 300 DPI PNG publication figures
│   ├── fig1_system_architecture.{pdf,png}        # End-to-end framework and cascade pipeline
│   ├── fig2_class_distribution.{pdf,png}         # Train/test partition class balances
│   ├── fig3_model_comparison.{pdf,png}           # Multi-model Accuracy, F1, and AUC comparisons
│   ├── fig4_confusion_matrices.{pdf,png}         # Confusion matrices across all 5 benchmark models
│   ├── fig5_roc_pr_curves.{pdf,png}              # Receiver Operating Characteristic & Precision-Recall curves
│   ├── fig6_shap_feature_importance.{pdf,png}    # Global mean |SHAP| attribution bar chart
│   ├── fig7_shap_summary_beeswarm.{pdf,png}      # SHAP summary beeswarm plot of feature impact
│   ├── fig8_local_shap_explanation.{pdf,png}     # Local sample-level waterfall explanations
│   ├── fig9_feature_reduction_comparison.{pdf,png} # Performance vs. feature subset size (Top-5 to Full)
│   └── fig10_computational_comparison.{pdf,png}  # Inference latency and memory profiling
│
├── src/                               # Modular Python source library
│   ├── __init__.py
│   ├── data_loader.py                 # Dataset loading and stratified splitting
│   ├── preprocessing.py               # Leakage-free zero-variance filtering and feature standardization
│   ├── feature_engineering.py         # 111-feature taxonomy definition and sentinel value management
│   ├── models.py                      # Model zoo (Logistic Regression, DT, Random Forest, SVM, XGBoost)
│   ├── train.py                       # 5-fold cross-validation and training orchestrator
│   ├── evaluate.py                    # Multi-metric evaluation (Accuracy, F1, Precision, Recall, AUC)
│   ├── explainability.py              # TreeSHAP explainer, global importance & local attributions
│   ├── feature_selection.py           # Feature reduction benchmarking (Top-5, Top-10, Top-20, Top-30)
│   ├── resource_measurement.py        # Micro-benchmarks for model memory, size, and inference latency
│   ├── export_latex.py                # Formatter converting experiment CSVs to LaTeX tables
│   ├── validate_results.py            # Automated mathematical verification script
│   ├── generate_paper_figures.py      # Matplotlib/Seaborn script generating Figures 1–10
│   ├── generate_manuscript_pdf.py     # ReportLab script compiling paper/PhishingURLDetector.pdf
│   └── predict_url.py                 # CLI tool for interactive URL inference and explanation
│
├── experiments/                       # Executable experiment & validation suite
│   ├── run_all.py                     # Master script executing the end-to-end experimental pipeline
│   ├── run_baseline.py                # 5-model baseline training and evaluation
│   ├── run_explainability.py          # Global and local SHAP computation
│   ├── run_feature_selection.py       # Dimensionality reduction and latency benchmark runner
│   ├── run_cascade_analysis.py        # Reproducibility script for two-tier cascade architecture
│   ├── run_path_analysis.py           # Evaluation of path-bearing vs. pathless URLs
│   ├── run_k_cv_seeds.py              # K-fold cross-validation sweep across multiple random seeds
│   ├── run_lr_svm_cosine.py           # Weight vector cosine similarity script for linear baselines
│   ├── run_shap_stability.py          # Multi-seed stability validation for SHAP feature rankings
│   └── check_experiments.py           # Feature prefix and dataset category validation
│
└── results/                           # Validated experiment outputs and checkpoints
    ├── metrics/                       # Benchmark metrics CSVs
    │   ├── model_comparison.csv
    │   ├── feature_selection_results.csv
    │   └── computational_benchmarks.csv
    ├── predictions/
    │   └── test_predictions.csv       # Test set probabilities and ground truth
    └── explanations/
        ├── shap_global_feature_importance.csv
        └── local_explanations.csv
```

---

## 4. Dataset Specification & Sentinel Handling

* **Benchmark Dataset**: Vrbančič et al. (2020), published in *Data in Brief* (Elsevier, [DOI: 10.1016/j.dib.2020.106438](https://doi.org/10.1016/j.dib.2020.106438)).
* **URL Count**: **58,645 total URLs** (30,647 Phishing [52.26%], 27,998 Legitimate [47.74%]).
* **Feature Space**: 111 raw attributes categorized into:
  - URL Lexical (20 features)
  - Domain Structural (21 raw $\rightarrow$ 8 non-zero variance)
  - Directory / Path Attributes (18 features)
  - File-Level Attributes (18 features)
  - Query Parameter Features (20 features)
  - Resolver / External Network Lookups (14 features)
  - **Retained Features**: **98 non-zero features** (84 purely static lexical + 14 external resolver).
* **Data Partitioning**: 80% Stratified Training (46,916 samples) / 20% Held-Out Test (11,729 samples: 6,129 phishing, 5,600 legitimate).
* **Sentinel Encoding Handling**: Features such as `directory_length`, `time_domain_activation`, and sub-delimiters use a `-1` sentinel to represent "not applicable" (e.g., domain with no path, masked WHOIS records, or resolver timeouts). Models and TreeSHAP treat these as informative structural indicators.
* **Leakage Guarantee**: All transformers, scalers, variance filters, and SHAP background distributions are fitted strictly on the training partition.

---

## 5. Key Experimental Results

All experiments are evaluated on the 11,729 held-out test partition.

### A. Multi-Model Benchmark Comparison (Full 98 Features)
| Model Architecture | Accuracy (%) | Precision (%) | Recall (%) | F1-Score (%) | ROC-AUC | PR-AUC | 5-Fold CV F1 (%) | Latency (ms/1k) | Model Size |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGBoost (Champion)** | **94.82%** | **94.88%** | **95.22%** | **95.05%** | **0.9879** | **0.9889** | **95.17% ± 0.13%** | **2.46 ± 0.20 ms** | **0.126 MB** |
| Random Forest | 94.30% | 94.03% | 95.12% | 94.57% | 0.9867 | 0.9878 | 94.79% ± 0.11% | 10.60 ± 0.31 ms | 4.068 MB |
| Decision Tree | 93.61% | 93.36% | 94.49% | 93.92% | 0.9668 | 0.9575 | 93.62% ± 0.17% | 0.53 ± 0.05 ms | 0.029 MB |
| Linear SVM (Platt Calibrated) | 89.99% | 89.10% | 92.12% | 90.58% | 0.9613 | 0.9637 | 90.45% ± 0.22% | 2.85 ± 0.20 ms | 0.006 MB |
| Logistic Regression | 89.97% | 89.23% | 91.91% | 90.55% | 0.9613 | 0.9637 | 90.48% ± 0.20% | 1.41 ± 0.16 ms | 0.004 MB |

*Statistical Significance*: McNemar's paired test comparing XGBoost and Random Forest on the 11,729 test set instances yielded $\chi^2 = 13.79$ ($p = 2.04 \times 10^{-4} < 0.001$), confirming statistically significant superiority.

---

### B. Feature Reduction Benchmarks (XGBoost)
| Configuration | Features (Net/Lex) | Accuracy (%) | F1-Score (%) | ROC-AUC | Inference (ms/1k) | Model Size | Throughput (q/s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| XGBoost (Full 98) | 14N / 84L | 94.82% | 95.05% | 0.9879 | 2.46 ± 0.20 ms | 0.126 MB | 406,318 |
| XGBoost (Top-30) | 12N / 18L | 94.74% | 94.97% | 0.9882 | 1.83 ± 0.07 ms | 0.134 MB | 546,448 |
| **XGBoost (Top-20)** | **11N / 9L** | **94.82%** | **95.05%** | **0.9876** | **1.67 ± 0.06 ms** | **0.130 MB** | **600,099** |
| XGBoost (Top-10) | 5N / 5L | 94.19% | 94.48% | 0.9859 | 1.57 ± 0.11 ms | 0.126 MB | 636,942 |
| XGBoost (Top-5) | 1N / 4L | 91.32% | 91.84% | 0.9723 | 1.59 ± 0.12 ms | 0.121 MB | 628,930 |
| **XGBoost (Lexical-84, Zero Net)** | **0N / 84L** | **89.68%** | **90.04%** | **0.9627** | **3.16 ± 0.43 ms** | **0.342 MB** | **316,002** |

*Key Insight*: Truncating the feature space from 98 to the **Top-20 SHAP features** maintains identical Accuracy (94.82%) and F1-Score (95.05%) while cutting inference latency by **32.1%** and expanding throughput to **600,000+ queries/second**.

---

### C. Two-Tier Uncertainty-Gated Cascade
To reconcile detection accuracy with the network latency of external resolver queries:
1. **Tier 1 (Lexical-84 Classifier)** parses purely in-memory URL string attributes (zero DNS/WHOIS queries). If predicted probability $\hat{p} < 0.10$ (confidently legitimate) or $\hat{p} > 0.90$ (confidently phishing), the URL is resolved immediately.
   - **Coverage**: Autonomously classifies **64.28%** of all URLs (7,539 / 11,729).
   - **Tier-1 Accuracy**: **97.78%** on resolved traffic.
   - **Tier-1 Phishing Recall**: **97.84%** ($4,082 / 4,172$).
2. **Tier 2 (Full Top-20 Classifier)**: Ambiguous traffic ($0.10 \le \hat{p} \le 0.90$) is deferred to Tier 2, where active resolver features (DNS TTL, SPF records, domain age) are queried.
3. **End-to-End Performance**: The combined cascade achieves **94.57% Accuracy and 94.81% F1-Score**, while eliminating resolver delays for nearly two-thirds of all queries.
4. **Latency Advantage**: Synchronous DNS resolution across 50 real-world domains averaged **93.81 ms median latency**, whereas in-memory lexical parsing executes in **11.6 microseconds per URL** (an 8,000× speedup).

---

## 6. Installation & Execution Guide

### Prerequisites
- Python 3.10 or higher
- Linux, macOS, or Windows

### Step 1: Environment Setup
```bash
# Clone the repository
git clone https://github.com/tanaychess/PhishingURLDetector.git
cd PhishingURLDetector

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate

# Install strictly pinned dependencies
pip install -r requirements.txt
```

### Step 2: Running Experiments & Reproducing Artifacts

You can reproduce specific benchmark components or run the entire pipeline with a single command:

* **Run Master End-to-End Pipeline**:
  ```bash
  python experiments/run_all.py
  ```
  *Executes*: Data preparation, multi-model baseline training, 5-fold CV, TreeSHAP attribution, feature reduction sweeps, figure generation, LaTeX table exports, and manuscript compilation.

* **Reproduce Table III (Model Comparison)**:
  ```bash
  python experiments/run_baseline.py
  ```

* **Reproduce Table V (Feature Reduction & Throughput Benchmarks)**:
  ```bash
  python experiments/run_feature_selection.py
  ```

* **Reproduce SHAP Explanations & Global Rankings**:
  ```bash
  python experiments/run_explainability.py
  ```

* **Reproduce Cascade Architecture Evaluation**:
  ```bash
  python experiments/run_cascade_analysis.py
  ```

* **Reproduce Path-Bearing vs. Pathless URL Dissection**:
  ```bash
  python experiments/run_path_analysis.py
  ```

* **Validate Cross-Validation Stability Across Seeds**:
  ```bash
  python experiments/run_k_cv_seeds.py
  ```

* **Validate TreeSHAP Multi-Seed Ranking Stability**:
  ```bash
  python experiments/run_shap_stability.py
  ```

* **Run Mathematical Verification Audit**:
  ```bash
  python src/validate_results.py
  ```

* **Compile the Publication Manuscript PDF**:
  ```bash
  python src/generate_manuscript_pdf.py
  ```
  *Output*: Directly saved to `paper/PhishingURLDetector.pdf`.

### Step 3: Interactive URL Inference & Explanation
Run the live prediction CLI to evaluate URLs and inspect their local TreeSHAP attribution breakdowns:
```bash
python src/predict_url.py --sample 5
```

---

## 7. Citation & Academic Reference

If you find this codebase or research useful in your work, please cite the manuscript:

```bibtex
@article{pathare2026phishingxai,
  author    = {Tanay Pathare},
  title     = {An Explainable Machine Learning Framework for Phishing Website Detection Using URL-Based Features},
  journal   = {Preprint},
  year      = {2026},
  url       = {https://github.com/tanaychess/PhishingURLDetector}
}
```

---

## 8. License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 9. Contact & Inquiries

For questions, collaborations, or reproduction assistance:
* **Tanay Pathare**  
* Department of Computer Science, Bhonsala Military College, Nashik, Maharashtra, India  
* Email: [tanaypathare1@gmail.com](mailto:tanaypathare1@gmail.com)  
* GitHub: [@tanaychess](https://github.com/tanaychess)
