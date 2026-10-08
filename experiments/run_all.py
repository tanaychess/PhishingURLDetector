"""
Master Experiment Pipeline: Executes end-to-end research workflow from data loading to validation and LaTeX table export.
"""

import os
import sys
import shutil
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_config, load_dataset, split_and_save_data
from src.preprocessing import PhishingPreprocessor
from src.train import train_and_evaluate_all
from src.explainability import run_shap_analysis
from src.feature_selection import run_feature_selection_experiments
from src.resource_measurement import benchmark_computational_resources
from src.generate_paper_figures import (
    plot_system_architecture,
    plot_class_distribution,
    plot_model_comparison,
    plot_confusion_matrices,
    plot_roc_pr_curves
)
from src.export_latex import export_all_latex_tables
from src.validate_results import validate_all_results

def run_master_pipeline():
    total_start = time.perf_counter()
    print("================================================================================")
    print("       STARTING COMPLETE EXPLAINABLE PHISHING RESEARCH PIPELINE")
    print("       Author: Tanay Samson Pathare (Bhonsala Military College)")
    print("================================================================================")
    
    config = load_config()
    fig_dir = config["paths"]["figures"]
    overleaf_fig_dir = config["paths"]["paper_figures"]
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(overleaf_fig_dir, exist_ok=True)
    
    # 1. Load Data
    print("\n[PHASE 1] Loading raw dataset...")
    df = load_dataset(config["dataset"]["raw_path"], config["dataset"]["target_column"])
    
    # 2. Data Split
    print("\n[PHASE 2] Splitting into Stratified Train/Test sets...")
    X_train, X_test, y_train, y_test = split_and_save_data(df, config)
    
    # 3. Preprocessing
    print("\n[PHASE 3] Preprocessing and feature verification...")
    preprocessor = PhishingPreprocessor(remove_constant=True, scale_features=False)
    X_train_df = preprocessor.fit_transform(X_train, return_df=True)
    X_test_df = preprocessor.transform(X_test, return_df=True)
    feature_names = preprocessor.feature_names
    
    # 4. Train and Evaluate Baseline Models
    print("\n[PHASE 4] Executing 5-Model Benchmark and 5-Fold Cross Validation...")
    results_df, trained_models, test_predictions, test_probabilities, latency_records = train_and_evaluate_all(
        X_train_df, y_train, X_test_df, y_test, config, feature_names
    )
    
    # 5. Generate Diagnostic Visuals (Figs 1-5)
    print("\n[PHASE 5] Generating system architecture, class distribution, and ROC/PR figures...")
    plot_system_architecture(fig_dir)
    plot_class_distribution(y_train, y_test, fig_dir)
    plot_model_comparison(results_df, fig_dir)
    plot_confusion_matrices(y_test, test_predictions, fig_dir)
    plot_roc_pr_curves(y_test, test_probabilities, fig_dir)
    
    # 6. SHAP Explainability (Figs 6-8)
    print("\n[PHASE 6] Running TreeSHAP Explainability and Attribution Analysis...")
    xgb_model = trained_models["XGBoost"]
    global_importance_df, local_df = run_shap_analysis(
        xgb_model, X_train_df, X_test_df, y_test, config, feature_names
    )
    
    # 7. Feature Reduction Benchmarking (Fig 9)
    print("\n[PHASE 7] Running Dimensional Feature Selection Benchmarks...")
    fs_df, subset_models, subset_latencies = run_feature_selection_experiments(
        X_train_df, y_train, X_test_df, y_test, global_importance_df, config,
        trained_full_model=xgb_model, full_latency_stats=latency_records.get("XGBoost")
    )
    
    # 8. Computational Profiling (Fig 10)
    print("\n[PHASE 8] Profiling Computational Latency, Memory Footprint, and Throughput...")
    comp_df = benchmark_computational_resources(
        trained_models, X_test_df, config,
        subset_models=subset_models,
        model_latencies=latency_records,
        subset_latencies=subset_latencies
    )

    
    # 9. Copy Figures to Overleaf Directory
    print("\n[PHASE 9] Syncing high-resolution figures to Overleaf folder...")
    for f in os.listdir(fig_dir):
        if f.endswith(".png") or f.endswith(".pdf"):
            shutil.copy(os.path.join(fig_dir, f), os.path.join(overleaf_fig_dir, f))
    print(f"  Synced {len(os.listdir(fig_dir))} figure files to {overleaf_fig_dir}")
    
    # 10. Export LaTeX Tables
    print("\n[PHASE 10] Generating verified LaTeX tables from result CSVs...")
    export_all_latex_tables(config)
    
    # 11. Strict Scientific Validation
    print("\n[PHASE 11] Running Scientific Validation...")
    validate_all_results(config)
    
    total_elapsed = time.perf_counter() - total_start
    print(f"\n================================================================================")
    print(f"   ALL EXPERIMENTS COMPLETED SUCCESSFULLY IN {total_elapsed:.2f} SECONDS!")
    print(f"================================================================================\n")

if __name__ == "__main__":
    run_master_pipeline()
