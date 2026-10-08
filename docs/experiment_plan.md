# Experiment Plan: Explainable Machine Learning Framework for Phishing Website Detection

**Author**: Tanay Samson Pathare  
**Affiliation**: Department of Computer Science, Bhonsala Military College, Nashik, Maharashtra, India  
**Email**: tanaypathare1@gmail.com  

---

## 1. Experimental Overview
This document outlines the systematic, end-to-end experimental execution protocol for benchmarking machine learning models and evaluating TreeSHAP explainability on static URL features.

---

## 2. Step-by-Step Experiment Protocol

### Experiment 1: Dataset Partitioning & Preprocessing
- **Source**: Vrbančič et al. (2020) containing 58,645 instances.
- **Split**: 80% Stratified Training (46,916 samples), 20% Held-Out Test (11,729 samples).
- **Zero-Variance Filtering**: Prunes non-informative features on training set ($D' = 98$ features).
- **Z-Score Scaling**: Fitted strictly on training set for linear/SVM classifiers.

### Experiment 2: Multi-Model Benchmark (RQ1)
- Train and evaluate 5 distinct architectures:
  1. Logistic Regression (L2 penalty, $C=1.0$)
  2. Decision Tree (Gini impurity, max\_depth=12)
  3. Random Forest (100 estimators, max\_depth=15)
  4. Linear SVM (Platt calibrated with 3-fold CV)
  5. XGBoost (100 estimators, max\_depth=6, $\eta=0.1$)
- Perform 5-Fold Stratified Cross-Validation on training set.
- Evaluate on 11,729 held-out test instances across Accuracy, Precision, Recall, F1-Score, ROC-AUC, and PR-AUC.

### Experiment 3: TreeSHAP Game-Theoretic Explainability (RQ2, RQ5)
- Initialize TreeSHAP on champion XGBoost model.
- Compute global mean absolute SHAP values: $I_j = \frac{1}{N_{\text{exp}}} \sum_{i} |\phi_j(\mathbf{x}_i)|$.
- Generate SHAP feature importance bar plot and beeswarm summary plot.
- Extract local instance explanations for individual phishing and benign test queries.

### Experiment 4: SHAP-Guided Feature Reduction (RQ3)
- Evaluate XGBoost performance across 5 ranked subsets:
  1. Full Model (98 features)
  2. Top-30 Features
  3. Top-20 Features
  4. Top-10 Features
  5. Top-5 Features
- Measure Accuracy, Precision, Recall, F1-Score, ROC-AUC, and inference latency across all subsets.

### Experiment 5: Computational Resource Benchmarking (RQ4)
- Measure training duration (seconds).
- Profile batch inference latency in milliseconds per 1,000 queries.
- Measure serialized in-memory model storage footprint (MB).
- Calculate continuous throughput (queries/second).

---

## 3. Reproduction Command
```bash
python experiments/run_all.py
```
