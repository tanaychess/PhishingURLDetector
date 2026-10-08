# Research Plan: An Explainable Machine Learning Framework for Phishing Website Detection Using URL-Based Features

**Author**: Tanay Samson Pathare  
**Affiliation**: Department of Computer Science, Bhonsala Military College, Nashik, Maharashtra, India  
**Email**: tanaypathare1@gmail.com  

---

## 1. Executive Summary & Research Motivation
Phishing attacks represent one of the most persistent attack vectors in modern cybersecurity, causing billions of dollars in annual financial and identity theft damages. While conventional security systems rely heavily on blacklist lookups (e.g., Google Safe Browsing, PhishTank), blacklists exhibit significant latency (often 2 to 48 hours) in indexing newly minted zero-hour phishing domains. 

Machine learning classifiers offer automated detection capabilities for unseen URLs. However, typical deployments face two critical roadblocks:
1. **The "Black-Box" Trust Barrier**: High accuracy without interpretability prevents Security Operations Center (SOC) analysts and end-users from validating predictions or understanding false positives.
2. **Computational Overhead & Content Extraction Risks**: Systems requiring full web-page crawling or heavy deep neural networks introduce unacceptable network latency and expose clients to client-side exploit payloads.

This research formulates an end-to-end, lightweight, explainable machine-learning framework using purely static URL-based lexical and structural characteristics. It couples high-performance tree ensembles with Shapley Additive Explanations (SHAP) and rigorous feature-reduction experiments to answer whether ultra-low-dimensional feature spaces can sustain high-fidelity detection with minimal latency.

---

## 2. Research Questions (RQs)
- **RQ1 (Model Superiority)**: Which machine learning architecture (Logistic Regression, Decision Tree, Random Forest, Linear SVM, or XGBoost) provides the highest discriminative performance across Accuracy, F1-Score, and ROC-AUC on static URL features?
- **RQ2 (Attribution & Explainability)**: Which URL-based lexical and structural features contribute most decisively to phishing classifications under axiomatic SHAP attribution?
- **RQ3 (Feature Reduction Viability)**: Can a substantially reduced subset of top SHAP features (e.g., 20, 10, or 5 features from 111) maintain competitive classification performance while reducing computational latency?
- **RQ4 (Computational Efficiency)**: What are the computational runtime, memory footprints, and inference latency trade-offs between full and reduced feature sets?
- **RQ5 (Local Interpretability)**: How effectively can local TreeSHAP explanations assist human triage by translating numeric risk scores into actionable URL component attributions?

---

## 3. Dataset Selection & Justification
- **Primary Dataset**: Vrbančič et al. (2020), published in *Data in Brief* (Elsevier, DOI: 10.1016/j.dib.2020.106438).
- **Sample Count**: 58,645 total instances (30,647 phishing [52.26%], 27,998 legitimate [47.74%]).
- **Feature Space**: 111 static features covering URL-, domain-, path-, directory-, parameter-, and resolver-level properties.
- **Academic Merit**: Features are entirely static, requiring zero active browser code execution, ensuring safe, zero-risk feature extraction.

---

## 4. Methodological Framework
1. **Data Preprocessing & Split**: Stratified 80/20 train/test split (46,916 training instances, 11,729 test instances). All scalers and transformers are fitted strictly on the training partition to prevent data leakage.
2. **Classifier Implementations**:
   - *Baseline Linear Classifier*: Regularized Logistic Regression (L2 penalty)
   - *Interpretable White-Box Tree*: Decision Tree (depth-constrained)
   - *Ensemble Bagging*: Random Forest (100 estimators)
   - *Maximum-Margin Classifier*: Linear Support Vector Machine (LinearSVC)
   - *Gradient Boosted Ensembles*: XGBoost (depth 6, colsample 0.8, subsample 0.8)
3. **Explainability Architecture**:
   - Axiomatic TreeSHAP implementation for XGBoost and Random Forest.
   - Extraction of global mean absolute SHAP values across all test samples.
   - Generation of local waterfall/force attributions for individual phishing and legitimate URLs.
4. **Feature Selection Strategy**:
   - SHAP-guided ranking of features.
   - Evaluation of 5 feature subsets: Full (98 features), Top-30, Top-20, Top-10, Top-5.
5. **Computational Benchmarking**:
   - Training duration (seconds).
   - Inference latency per 1,000 queries (milliseconds).
   - In-memory model footprint (megabytes).

---

## 5. Deliverables & Impact
1. Full Python codebase with modular architecture in `src/`.
2. Single-command reproducible execution via `python experiments/run_all.py`.
3. Validated CSV results in `results/metrics/` with validation script `src/validate_results.py`.
4. High-resolution figures in `figures/` and automated LaTeX tables in `paper/overleaf/tables/`.
5. Complete, compilable, Overleaf-ready IEEE-format manuscript in `paper/overleaf/` and `paper/final/Phishing_Website_XAI.pdf`.
6. Academic defense questions and presentation materials in `docs/`.
