# Research Presentation Deck: Academic Research Defense

**Title**: An Explainable Machine Learning Framework for Phishing Website Detection Using URL-Based Features  
**Author / Presenter**: Tanay Samson Pathare  
**Affiliation**: Department of Computer Science, Bhonsala Military College, Nashik, Maharashtra, India  
**Email**: tanaypathare1@gmail.com  
**Slide Format**: 12 Presentation Slides with Detailed Speaker Notes  

---

## Slide 1: Title & Academic Affiliation
- **Slide Title**: An Explainable Machine Learning Framework for Phishing Website Detection Using URL-Based Features
- **Visuals**: Clean academic header, conceptual schematic of a URL passing through an interpretable ML shield.
- **Presenter Details**: Tanay Samson Pathare, Department of Computer Science, Bhonsala Military College.
- **Speaker Notes**:  
  *"Good morning respected chairperson, evaluators, and delegates. Today, I am presenting my research titled 'An Explainable Machine Learning Framework for Phishing Website Detection Using URL-Based Features'. This work tackles the dual challenge of zero-hour phishing detection and machine learning opacity using lightweight static URL analysis and game-theoretic explainability."*

---

## Slide 2: Problem Statement & Real-World Motivation
- **Key Bullet Points**:
  - Phishing accounts for over 80% of reported enterprise security compromises worldwide.
  - Traditional Blacklists (Google Safe Browsing, PhishTank) exhibit a 2–48 hour discovery window latency.
  - Zero-day phishing campaigns achieve their maximum exploitation within the first 2 hours of deployment.
  - Content-based crawlers expose clients to drive-by malware exploits and introduce 500ms–2s network latency.
- **Visual**: Diagram showing the 2–48 hour vulnerability gap of blacklists vs. instant static ML inference.
- **Speaker Notes**:  
  *"Phishing remains the most pervasive attack vector in modern cybersecurity. While blacklists are highly accurate for known domains, they cannot protect users during the initial 2 to 48 hours required to discover and index new zero-day campaigns. Furthermore, rendering remote web pages for content inspection introduces unacceptable latency and exposes analysis engines to malicious payloads. We need a proactive, safe, and instant screening solution."*

---

## Slide 3: The Research Gap & Core Questions
- **Key Bullet Points**:
  - **The Black-Box Dilemma**: Complex ML classifiers provide high accuracy but zero causal explanation, causing alert fatigue and distrust in SOC environments.
  - **Feature Bloat**: High-dimensional feature spaces introduce latency bottlenecks on high-throughput network gateways.
  - **Central Research Question**: *Can explainable machine-learning models accurately detect phishing URLs while providing understandable information about which URL characteristics contribute to the prediction?*
- **Visual**: "Black-Box ML" vs. "Explainable ML (TreeSHAP)" comparison block.
- **Speaker Notes**:  
  *"In a modern Security Operations Center, a binary 'phishing' flag without explanation is insufficient. Analysts need to know why an alert fired to take forensic action. My research questions specifically investigate which ML model performs best, which URL features dominate predictions, whether we can drastically prune the feature space without sacrificing accuracy, and how fast the resulting model can run."*

---

## Slide 4: Proposed System Architecture
- **Key Bullet Points**:
  - Purely static, 4-stage processing pipeline:
    1. Static Feature Extraction (111 Lexical, Domain, Path, Resolver Metrics)
    2. Multi-Model Classification (LR, DT, RF, SVM, XGBoost)
    3. TreeSHAP Attribution & Interpretability Engine
    4. SHAP-Guided Feature Reduction & Latency Profiling
- **Visual**: High-resolution rendering of Fig. 1 (System Architecture Block Diagram).
- **Speaker Notes**:  
  *"Here is my end-to-end architecture. The entire workflow operates on static URL strings and passive DNS metadata, requiring zero HTTP page rendering. The pipeline passes extracted features to ensemble classifiers, while TreeSHAP extracts both global feature rankings and local instance-level forensic justifications."*

---

## Slide 5: Dataset & Feature Engineering Taxonomy
- **Key Bullet Points**:
  - Benchmark Dataset: Vrbančič et al. (*Data in Brief*, Elsevier, 2020).
  - Total Sample Size: **58,645 URLs** (30,647 Phishing [52.26%], 27,998 Benign [47.74%]).
  - Split: 80% Stratified Train ($N=46,916$) / 20% Held-Out Test ($N=11,729$). Zero data leakage.
  - 6 Structured Feature Families: URL Lexical, Domain Structural, Directory/Path, File-Level, Query Parameters, and Resolver Metrics.
- **Visual**: Dataset class distribution bar chart (Fig. 2) and feature family pie chart.
- **Speaker Notes**:  
  *"I utilized a rigorously peer-reviewed dataset of 58,645 URLs. I enforced an 80/20 stratified split, ensuring that all scalers and variance filters were fitted strictly on the training partition. The 111 features capture everything from token lengths and delimiter frequencies to domain activation age and DNS TTL."*

---

## Slide 6: Multi-Model Comparative Benchmarking
- **Key Bullet Points**:
  - Evaluated 5 diverse algorithms on 11,729 held-out test samples with 5-Fold Cross-Validation:
    - **XGBoost**: **94.82% Accuracy**, **95.05% F1-Score**, **0.9879 ROC-AUC** (5-Fold CV F1: $95.17\% \pm 0.13\%$)
    - **Random Forest**: 94.30% Accuracy, 94.57% F1-Score, 0.9867 ROC-AUC
    - **Decision Tree**: 93.61% Accuracy, 93.92% F1-Score, 0.9668 ROC-AUC
    - **Linear SVM**: 89.99% Accuracy, 90.58% F1-Score, 0.9613 ROC-AUC
    - **Logistic Regression**: 89.97% Accuracy, 90.55% F1-Score, 0.9613 ROC-AUC
- **Visual**: Model performance bar chart (Fig. 3) and ROC / PR Curves (Fig. 5).
- **Speaker Notes**:  
  *"Looking at the empirical benchmark results, tree ensembles clearly outperform linear classifiers. XGBoost achieved the highest performance across all metrics with an F1-score of 95.05% and an ROC-AUC of 0.9879. The 5-fold cross-validation standard deviation of just 0.13% proves that the model generalizes robustly across folds."*

---

## Slide 7: Confusion Matrix & Error Analysis
- **Key Bullet Points**:
  - XGBoost Test Performance ($N=11,729$):
    - True Positives ($TP$): **5,836** (95.22% Recall)
    - True Negatives ($TN$): **5,285** (94.38% Specificity)
    - False Positives ($FP$): **315** ($\text{FPR} = 5.62\%$)
    - False Negatives ($FN$): **293** ($\text{FNR} = 4.78\%$)
  - Low False Negative rate ensures minimal victim compromise.
- **Visual**: Side-by-side Confusion Matrix heatmaps for XGBoost and Random Forest (Fig. 4).
- **Speaker Notes**:  
  *"Analyzing the confusion matrix on 11,729 unseen test samples, XGBoost successfully caught 5,836 phishing URLs with a False Negative Rate of only 4.78%. Error analysis showed that the few missed phishing sites occurred when attackers hosted forms on legitimate cloud infrastructure like AWS S3 or Google Forms."*

---

## Slide 8: Global Feature Explainability with TreeSHAP
- **Key Bullet Points**:
  - TreeSHAP computes exact Shapley attributions in polynomial time $\mathcal{O}(TL\Delta^2)$.
  - **Top Dominant Features**:
    1. `directory_length` ($\text{Mean } |\text{SHAP}| = 1.1390$) $\rightarrow$ Deep paths strongly signal phishing.
    2. `time_domain_activation` ($1.0298$) $\rightarrow$ Mature domains indicate legitimacy; new domains indicate phishing.
    3. `qty_slash_url` ($0.7686$) $\rightarrow$ High slash counts reflect URL nesting obfuscation.
    4. `length_url` ($0.7131$) $\rightarrow$ Long URLs embed spoofed brand tokens.
- **Visual**: SHAP global ranking bar chart (Fig. 6) and SHAP summary beeswarm plot (Fig. 7).
- **Speaker Notes**:  
  *"Through TreeSHAP, we open the black box. The global beeswarm plot reveals that directory length and domain activation age are the two most critical drivers. Long directory paths push the model heavily toward a phishing classification, while long-established domain ages push the prediction toward legitimate."*

---

## Slide 9: Local Instance Explainability for SOC Triage
- **Key Bullet Points**:
  - Converts opaque numeric predictions into intuitive, feature-by-feature risk explanations.
  - Instance Example: Test URL predicted as Phishing with $P(\text{Phishing}) = 0.998$.
  - Positive Forces (+Risk): Excessive directory length (+0.82) and zero-day domain registration (+0.64).
  - Negative Forces (-Risk): Valid TLS certificate structure (-0.12).
- **Visual**: Local instance SHAP attribution bar plot (Fig. 8).
- **Speaker Notes**:  
  *"For incident response, TreeSHAP produces local instance attributions like this. When an alarm is triggered, the SOC analyst immediately sees the exact features responsible: in this case, a deeply nested directory path combined with a domain registered just days prior. This transforms automated ML from a black-box into an auditable decision-support tool."*

---

## Slide 10: Dimensionality Reduction & Feature Selection Trade-Offs
- **Key Bullet Points**:
  - Evaluated 5 SHAP-ranked feature subsets: Full (98), Top-30, Top-20, Top-10, and Top-5.
  - **Top-20 Subset Performance**:
    - Retains **99.89%** of Full Model F1-Score (**95.00%** vs. 95.10%).
    - Reduces feature dimensionality by **79.6%** (from 98 to 20).
    - Reduces inference latency by **36.4%** (from 2.39 ms to 1.52 ms per 1k URLs).
    - Halves training time (0.77s vs. 1.57s).
- **Visual**: Dual-axis Feature Reduction Trade-Off Plot (Fig. 9).
- **Speaker Notes**:  
  *"A central research question was: can we prune the feature space? My experiments proved that selecting just the Top-20 SHAP features preserves 99.89% of F1-score while slashing latency by over 36% and reducing feature extraction overhead by nearly 80%. This confirms that an ultra-compact model is practically viable for high-speed edge devices."*

---

## Slide 11: Computational Efficiency & Deployment Profile
- **Key Bullet Points**:
  - **Serialized Model Footprint**:
    - XGBoost: **0.126 MB** (vs. Random Forest: 4.07 MB).
    - Decision Tree: 0.029 MB.
  - **Inference Latency & Throughput**:
    - Full XGBoost: 2.43 ms per 1,000 queries (**412,183 URLs/sec**).
    - Top-20 XGBoost: 1.52 ms per 1,000 queries (**657,894 URLs/sec**).
  - Suitable for direct integration into DNS resolvers, web proxies, and client-side browser extensions.
- **Visual**: Computational efficiency and model size comparison (Fig. 10).
- **Speaker Notes**:  
  *"From a software engineering perspective, the Top-20 XGBoost model has a footprint of just 126 kilobytes and can process over 650,000 URLs per second on standard CPU hardware. This makes it ideal for deployment in memory-constrained environments like firewall appliances and DNS servers without requiring dedicated GPU acceleration."*

---

## Slide 12: Conclusion & Future Roadmap
- **Key Takeaways**:
  - Successfully built and validated an explainable, lightweight phishing detection framework.
  - XGBoost achieved champion performance (94.82% accuracy, 95.05% F1, 0.9879 ROC-AUC).
  - TreeSHAP identified directory depth and domain age as dominant predictive signals.
  - Top-20 feature pruning delivers sub-millisecond screening with 99.89% F1 retention.
  - 100% reproducible pipeline, verified results, and Overleaf-ready IEEE manuscript.
- **Future Roadmap**:
  - Online adaptive streaming against concept drift.
  - Unicode homoglyph character embeddings.
  - WebAssembly browser extension deployment.
- **Speaker Notes**:  
  *"In conclusion, my research demonstrates that explainable, static URL-based machine learning provides a highly accurate, ultra-fast, and safe counter-phishing defense. I have prepared an Overleaf-ready IEEE manuscript and fully reproducible codebase. Thank you for your time, and I now welcome your questions."*
