# Research Defense: Comprehensive Academic Viva Voce Guide

**Research Title**: An Explainable Machine Learning Framework for Phishing Website Detection Using URL-Based Features  
**Author / Researcher**: Tanay Samson Pathare  
**Affiliation**: Department of Computer Science, Bhonsala Military College, Nashik, Maharashtra, India  
**Email**: tanaypathare1@gmail.com  

---

## Category 1: Research Motivation & Problem Definition

### Q1: What is the core problem your research addresses, and why is it significant?
**Answer**:  
The research addresses the vulnerability window and trust barrier in automated phishing website detection. Phishing causes billions of dollars in annual enterprise and consumer fraud. Traditional countermeasures rely on signature blacklists (e.g., Google Safe Browsing, PhishTank), which suffer from a 2–48 hour discovery latency, leaving users unprotected against zero-hour attacks. While machine learning (ML) can detect unseen phishing URLs proactively, existing models function as opaque "black boxes" that security operations center (SOC) analysts cannot trust or verify. Furthermore, content-based detection requires rendering malicious web pages, introducing client exploit risks and network latency. My research solves this by building an explainable, lightweight framework using purely static URL features.

---

### Q2: Why did you choose static URL features instead of analyzing web-page content or screenshots?
**Answer**:  
Static URL analysis has three major advantages:
1. **Zero Client-Side Risk**: It does not execute JavaScript or fetch remote HTML payloads, completely eliminating the danger of drive-by malware infections.
2. **Ultra-Low Latency**: It requires zero network round-trip time to the target host, enabling sub-millisecond classification suitable for inline firewall proxies and DNS resolvers.
3. **Resilience to Cloaking**: Phishing attackers often deploy IP geofencing, CAPTCHAs, or user-agent filters to hide malicious HTML from automated web crawlers. Static URL analysis bypasses these cloaking techniques because the URL itself cannot be hidden.

---

### Q3: What is the central research question (RQ) and its supporting sub-questions?
**Answer**:  
**Central RQ**: *Can explainable machine-learning models accurately detect phishing URLs while providing understandable information about which URL characteristics contribute to the prediction?*  
- **RQ1**: Which ML architecture achieves the strongest discriminative performance on static URL features?
- **RQ2**: Which specific URL characteristics contribute most decisively to phishing classifications under game-theoretic SHAP attributions?
- **RQ3**: Can a reduced feature subset maintain competitive classification performance while reducing computational overhead?
- **RQ4**: What is the computational throughput, memory footprint, and inference latency across full and reduced feature spaces?
- **RQ5**: How effectively can local TreeSHAP explanations assist human triage in incident response?

---

### Q4: How is your work novel compared to existing literature?
**Answer**:  
Rather than claiming to be the first to apply ML to phishing, my novelty lies in:
1. Conducting an axiomatic, game-theoretic TreeSHAP feature attribution analysis on a high-dimensional static dataset (58,645 URLs across 111 structured metrics).
2. Proving empirically that SHAP-directed feature pruning allows an 79.6% reduction in feature dimensions (from 98 to 20 features) while retaining 99.89% of full model F1-score (95.00% vs. 95.10%).
3. Providing an ultra-lightweight footprint (0.126 MB model size, 1.52 ms latency per 1k URLs) capable of screening over 650,000 URLs/second for real-time edge security.

---

## Category 2: Dataset, Preprocessing & Data Integrity

### Q5: What dataset did you use, and what is its provenance?
**Answer**:  
I used the peer-reviewed benchmark dataset published by Grega Vrbančič, Iztok Fister Jr, and Vili Podgorelec in *Data in Brief* (Elsevier, 2020, DOI: 10.1016/j.dib.2020.106438). It contains 58,645 total URLs, consisting of 30,647 verified phishing URLs (collected from PhishTank and OpenPhish) and 27,998 legitimate URLs (sampled from Alexa top domains).

---

### Q6: How did you split the dataset, and how did you prevent data leakage?
**Answer**:  
I utilized an 80/20 Stratified Train/Test split:
- **Training partition**: 46,916 samples (24,518 phishing [52.26%], 22,398 legitimate [47.74%]).
- **Testing partition**: 11,729 samples (6,129 phishing [52.26%], 5,600 legitimate [47.74%]).  
**Data Leakage Prevention**: All transformations (zero-variance filtering, standard scalers, imputation parameters, and SHAP rankings) were fitted strictly on the training partition and applied downstream to the test partition. No test samples were ever observed during training or feature selection.

---

### Q7: What feature categories exist in your dataset?
**Answer**:  
The 111 features span six structured families:
1. **URL Lexical**: Total length, dot counts, hyphen counts, slash counts, delimiter frequencies.
2. **Domain Structural**: Domain length, subdomain counts, vowels, presence of IP address.
3. **Directory & Path**: Directory path length, nesting depth, special characters.
4. **File-Level**: Target file extension length and dot frequencies.
5. **Query & Parameter**: Count of query parameters and special characters in query strings.
6. **Resolver Metadata**: Domain activation age, expiration time, TTL, ASN, and nameserver counts.

---

### Q8: How did you handle class balance? Was SMOTE necessary?
**Answer**:  
The dataset is inherently well-balanced: 52.26% phishing and 47.74% legitimate. Because the class ratio is nearly 1:1, synthetic oversampling techniques such as SMOTE were unnecessary and would have introduced artificial interpolation artifacts. Stratified sampling was used to preserve this balance in both train and test partitions.

---

## Category 3: Machine Learning Models & Algorithms

### Q9: Which machine learning models did you evaluate, and why?
**Answer**:  
I evaluated five representative paradigms:
1. **Logistic Regression**: Baseline linear probabilistic classifier with L2 regularization.
2. **Decision Tree**: Interpretable white-box tree model (depth-constrained).
3. **Random Forest**: Ensemble bagging classifier with 100 decorrelated trees.
4. **Linear Support Vector Machine (Linear SVM)**: Maximum-margin classifier with Platt probability calibration.
5. **XGBoost (eXtreme Gradient Boosting)**: State-of-the-art gradient-boosted decision tree ensemble using exact second-order Taylor expansion and histogram split finding.

---

### Q10: Why didn't you use deep neural networks (CNNs, Transformers)?
**Answer**:  
For tabular cybersecurity features:
1. Tree-based ensembles (XGBoost, Random Forest) consistently match or exceed deep learning performance on tabular data without requiring massive parameter tuning.
2. Deep networks have high computational overhead (large memory footprint and GPU requirements), making them unsuitable for edge gateways and router-level firewalls.
3. TreeSHAP provides fast, exact polynomial-time game-theoretic explanations on tree ensembles ($\mathcal{O}(T L \Delta^2)$), whereas deep learning XAI methods (e.g., Integrated Gradients, DeepSHAP) require approximations and high compute runtime.

---

### Q11: How do you configure and tune hyperparameters?
**Answer**:  
All hyperparameters are systematically managed in `config/config.yaml`:
- **XGBoost**: 100 estimators, max\_depth=6, learning\_rate=0.1, subsample=0.8, colsample\_bytree=0.8, tree\_method="hist".
- **Random Forest**: 100 trees, max\_depth=15, min\_samples\_split=5, min\_samples\_leaf=2.
- **Decision Tree**: max\_depth=12, min\_samples\_split=10, min\_samples\_leaf=5.
- **Logistic Regression**: L-BFGS solver, C=1.0, max\_iter=1000.
- **Linear SVM**: C=1.0, max\_iter=2000, calibrated via 3-fold cross-validation.

---

## Category 4: Performance Evaluation & Results

### Q12: What were the quantitative results of your multi-model comparison?
**Answer**:  
Evaluated on the 11,729 held-out test samples:
- **XGBoost**: **94.82% Accuracy**, **94.88% Precision**, **95.22% Recall**, **95.05% F1-Score**, **0.9879 ROC-AUC**, 5-fold CV F1: $95.17\% \pm 0.13\%$.
- **Random Forest**: 94.30% Accuracy, 94.03% Precision, 95.12% Recall, 94.57% F1-Score, 0.9867 ROC-AUC.
- **Decision Tree**: 93.61% Accuracy, 93.36% Precision, 94.49% Recall, 93.92% F1-Score, 0.9668 ROC-AUC.
- **Linear SVM**: 89.99% Accuracy, 89.10% Precision, 92.12% Recall, 90.58% F1-Score, 0.9613 ROC-AUC.
- **Logistic Regression**: 89.97% Accuracy, 89.23% Precision, 91.91% Recall, 90.55% F1-Score, 0.9613 ROC-AUC.

---

### Q13: What were the confusion matrix values for your best model (XGBoost)?
**Answer**:  
On 11,729 test samples:
- **True Positives ($TP$)**: 5,836 (correctly detected phishing URLs)
- **True Negatives ($TN$)**: 5,285 (correctly identified benign URLs)
- **False Positives ($FP$)**: 315 (benign URLs wrongly flagged as phishing, $\text{FPR} = 5.62\%$)
- **False Negatives ($FN$)**: 293 (phishing URLs missed, $\text{FNR} = 4.78\%$)

---

### Q14: Why is Recall particularly critical in phishing detection?
**Answer**:  
In cybersecurity, a False Negative (missed phishing site) allows an end-user to access a credential-harvesting portal, leading to identity theft or financial loss. A False Positive (blocking a legitimate site) merely requires user whitelisting or secondary verification. Therefore, achieving a high Recall (95.22% in XGBoost) is essential to minimize victim compromise.

---

## Category 5: Explainability & TreeSHAP

### Q15: What is SHAP, and what theoretical foundation does it rely on?
**Answer**:  
SHAP (SHapley Additive exPlanations), formulated by Lundberg and Lee (NeurIPS 2017), is an Explainable AI method grounded in cooperative game theory. It calculates Shapley values, which uniquely satisfy four desirable mathematical properties: **Local Accuracy** (additive efficiency), **Missingness**, **Consistency**, and **Symmetry**. It assigns each feature an attribution value $\phi_j$ representing its marginal contribution to shifting the model prediction from the base expected value to the final output.

---

### Q16: What is the difference between TreeSHAP and KernelSHAP?
**Answer**:  
- **KernelSHAP** is model-agnostic but relies on sampling permutations, requiring exponential time $\mathcal{O}(2^M)$ or slow sampling approximations.
- **TreeSHAP** is an exact algorithm tailored for decision trees and tree ensembles. By tracking decision paths recursively through the tree structures, it computes exact Shapley values in low polynomial time $\mathcal{O}(T L \Delta^2)$, where $T$ is the number of trees, $L$ is max leaves, and $\Delta$ is tree depth.

---

### Q17: What are the top features identified by SHAP, and what are their cybersecurity rationales?
**Answer**:  
The top features and their mean absolute SHAP values are:
1. **`directory_length` (1.1390)**: Phishers construct long nested directories (e.g., `/secure/login/auth/`) to mimic authentic enterprise pathways.
2. **`time_domain_activation` (1.0298)**: Established benign domains have years of registration history, whereas phishing campaigns deploy transient, newly activated zero-hour domains.
3. **`qty_slash_url` (0.7686)**: Excess slashes indicate deeply nested obfuscation structures.
4. **`length_url` (0.7131)**: Phishing URLs are significantly longer to embed authentication redirect tokens and brand spoof keywords.
5. **`qty_dot_domain` (0.5038)**: Subdomain spoofing (e.g., `paypal.com.account-update.xyz`).
6. **`ttl_hostname` (0.3041)**: Low TTL values are used in fast-flux DNS rotation to evade IP blocklists.

---

### Q18: What is the difference between global and local SHAP explanations?
**Answer**:  
- **Global Explanation**: Aggregates the mean absolute SHAP values across the entire test dataset to determine overall feature importance and directional tendencies (via bar and beeswarm plots).
- **Local Explanation**: Generates instance-specific attributions for a single URL query, showing the exact positive (phishing-pushing) and negative (benign-pushing) forces for that specific prediction.

---

## Category 6: Feature Selection & Computational Benchmarks

### Q19: What did your feature selection experiments reveal?
**Answer**:  
I evaluated XGBoost on five SHAP-ranked subsets:
- **Full (98 features)**: 94.87% Accuracy, 95.10% F1-Score, 2.39 ms / 1k latency.
- **Top-30**: 94.63% Accuracy, 94.87% F1-Score, 1.62 ms / 1k latency.
- **Top-20**: **94.76% Accuracy**, **95.00% F1-Score**, **1.52 ms / 1k latency**.
- **Top-10**: 94.05% Accuracy, 94.33% F1-Score, 1.39 ms / 1k latency.
- **Top-5**: 91.32% Accuracy, 91.84% F1-Score, 1.31 ms / 1k latency.  
**Key Finding**: The **Top-20 subset** preserves 99.89% of full model F1 performance while cutting feature dimensionality by 79.6% and accelerating inference latency by 36.4%.

---

### Q20: What are the memory footprints and query throughputs of your models?
**Answer**:  
- **XGBoost**: Model size = **0.126 MB**, Throughput = **412,183 queries/second** (2.43 ms per 1,000 URLs).
- **Decision Tree**: Model size = **0.029 MB**, Throughput = **1,548,183 queries/second** (0.65 ms per 1,000 URLs).
- **Random Forest**: Model size = **4.068 MB**, Throughput = **115,029 queries/second** (8.69 ms per 1,000 URLs).
- **Linear SVM**: Model size = **0.006 MB**, Throughput = **459,458 queries/second** (2.18 ms per 1,000 URLs).
- **Logistic Regression**: Model size = **0.004 MB**, Throughput = **804,707 queries/second** (1.24 ms per 1,000 URLs).

---

## Category 7: Limitations, Threats to Validity & Practical Deployment

### Q21: What are the primary limitations of your research?
**Answer**:  
1. **Adversarial Concept Drift**: Phishing campaigns continually evolve hosting tactics; static models require periodic re-training against live threat streams.
2. **Abuse of Legitimate Cloud Services**: When attackers host forms on legitimate infrastructure (e.g., Google Forms, GitHub Pages, Microsoft Azure), domain-level features appear benign.
3. **Unicode Homoglyph Attacks**: Advanced Internationalized Domain Name (IDN) spoofing (e.g., Cyrillic 'а' replacing Latin 'a') requires character-level token embeddings.
4. **Energy Measurement**: Hardware power consumption was inferred through runtime and CPU throughput rather than physical power meters.

---

### Q22: Why did some legitimate URLs trigger False Positives?
**Answer**:  
False Positives (315 samples) were predominantly caused by complex e-commerce tracking links, multi-hop affiliate advertising URLs, and CDN redirects that contain deep directory paths, excessive slashes, and numerous query parameters that syntactically resemble obfuscated phishing URLs.

---

### Q23: Why did some phishing URLs result in False Negatives?
**Answer**:  
False Negatives (293 samples) occurred when phishers utilized high-reputation shared hosting platforms (e.g., AWS S3, Google Firebase) or short, simple URLs without nested directory paths. In these cases, the domain activation age and minimal slash counts produced strong legitimate attributions that outweighed the malicious payload.

---

### Q24: How would you deploy this framework in a real enterprise security architecture?
**Answer**:  
The framework can be deployed at three integration tiers:
1. **DNS Resolver / Edge Gateway**: The Top-20 XGBoost model (0.126 MB) can inspect inbound DNS lookups at over 650,000 queries/second with sub-millisecond overhead.
2. **Email Security Proxy**: Inbound email URLs are statically parsed and scored before message delivery.
3. **SOC Incident Response Dashboard**: When an alarm triggers, the local SHAP waterfall plot is rendered directly in the SIEM/SOC console, allowing analysts to instantly verify the structural anomalies.

---

### Q25: What methodology guarantees experimental reproducibility in your framework?
**Answer**:  
I established strict reproducibility protocols:
1. Fixed random seeds (42) across splitting, cross-validation, and model training.
2. Centralized declarative configuration via `config/config.yaml`.
3. Modular Python architecture with a single-command master runner (`python experiments/run_all.py`).
4. Automated mathematical validation script (`src/validate_results.py`) verifying confusion matrix derivations.

---

### Q26: How did you ensure mathematical consistency across all reported metrics?
**Answer**:  
I implemented an automated verification module (`src/validate_results.py`) that strictly checks:
- $TP + TN + FP + FN = N_{\text{test}} = 11,729$.
- Calculated metrics exactly equal confusion matrix derivations within $10^{-3}$ tolerance.
- ROC-AUC and PR-AUC values lie within the $[0, 1]$ interval.
- SHAP rankings are strictly monotonic in descending order.

---

### Q27: How can the system be made resilient against adversarial evasion?
**Answer**:  
To resist adversarial perturbation (e.g., attackers deliberately shortening directory paths or adding benign tokens), the framework can incorporate:
1. **Adversarial Training**: Augmenting the training corpus with perturbed URL variations.
2. **Multi-View Ensembling**: Combining static lexical features with passive certificate transparency log monitoring.
3. **Adaptive Thresholding**: Dynamically shifting decision thresholds based on the target organization's risk tolerance.

---

### Q28: What is the impact of domain activation time on zero-hour detection?
**Answer**:  
Domain activation age (`time_domain_activation`) is the second most decisive feature (SHAP = 1.0298). Attackers predominantly register new domains hours before launching an attack. Therefore, a domain age $< 14$ days provides a powerful heuristic signal that shifts the log-odds heavily toward phishing.

---

### Q29: What future enhancements do you plan for this framework?
**Answer**:  
I plan to:
1. Develop an online continuous learning pipeline with streaming PhishTank and OpenPhish threat feeds.
2. Integrate character-level transformer embeddings (e.g., CANINE or ByT5) to detect multilingual Unicode homoglyph spoofing.
3. Package the model into a lightweight, client-side WebAssembly browser extension.

---

### Q30: What is your final concluding takeaway from this research?
**Answer**:  
Explainable, static URL-based machine learning with XGBoost and TreeSHAP offers a high-accuracy (94.82%), ultra-low-latency (1.52 ms/1k queries), and completely safe counter-phishing defense. By pruning to 20 key features, I achieve an enterprise-ready security framework that combines superior detection performance with human-interpretable forensic transparency.
