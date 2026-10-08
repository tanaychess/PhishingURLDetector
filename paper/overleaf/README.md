# Overleaf LaTeX Package: Explainable Phishing Website Detection

**Paper Title**: An Explainable Machine Learning Framework for Phishing Website Detection Using URL-Based Features  
**Author**: Tanay Samson Pathare  
**Affiliation**: Department of Computer Science, Bhonsala Military College, Nashik, Maharashtra, India  
**Email**: tanaypathare1@gmail.com  

---

## Instructions for Overleaf Upload

1. **Download the ZIP**: Locate the file `PhishingURLDetector_Overleaf.zip` in this directory or in `paper/`.
2. **Import into Overleaf**:
   - Log into [Overleaf](https://www.overleaf.com/).
   - Click **New Project** -> **Upload Project**.
   - Select `PhishingURLDetector_Overleaf.zip`.
3. **Compile**:
   - Set the compiler to **pdfLaTeX** (default).
   - Set the TeX Live version to **2024 / Latest**.
   - Click **Recompile**.

---

## Directory Structure

```text
overleaf/
├── main.tex                 # Master document (Author: Tanay Samson Pathare)
├── references.bib           # Verified BibTeX bibliography
├── IEEEtran.cls             # Official IEEE conference document class
├── sections/                # Modular paper sections
│   ├── introduction.tex
│   ├── related_work.tex
│   ├── methodology.tex
│   ├── experiments.tex
│   ├── results.tex
│   ├── discussion.tex
│   └── conclusion.tex
├── tables/                  # Automated LaTeX tables generated from experiment CSVs
│   ├── table1_dataset.tex
│   ├── table2_model_config.tex
│   ├── table3_model_comparison.tex
│   ├── table4_feature_selection.tex
│   ├── table5_computational_resources.tex
│   └── table6_top_shap_features.tex
└── figures/                 # Vector PDF and PNG high-resolution figures (300 DPI)
    ├── fig1_system_architecture.pdf
    ├── fig2_class_distribution.pdf
    ├── fig3_model_comparison.pdf
    ├── fig4_confusion_matrices.pdf
    ├── fig5_roc_pr_curves.pdf
    ├── fig6_shap_feature_importance.pdf
    ├── fig7_shap_summary_beeswarm.pdf
    ├── fig8_local_shap_explanation.pdf
    ├── fig9_feature_reduction_comparison.pdf
    └── fig10_computational_comparison.pdf
```
