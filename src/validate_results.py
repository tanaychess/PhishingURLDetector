"""
Scientific validation script: rigorously verifies mathematical integrity and consistency of experimental results.
"""

import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def validate_all_results(config):
    """
    Run automated sanity and mathematical consistency checks on all experimental outputs.
    """
    print("\n================ RUNNING SCIENTIFIC INTEGRITY VALIDATION ================")
    
    metrics_dir = config["paths"]["results_metrics"]
    exp_dir = config["paths"]["results_explanations"]
    fig_dir = config["paths"]["figures"]
    
    m_csv = os.path.join(metrics_dir, "model_comparison.csv")
    fs_csv = os.path.join(metrics_dir, "feature_selection_results.csv")
    shap_csv = os.path.join(exp_dir, "shap_global_feature_importance.csv")
    
    assert os.path.exists(m_csv), f"Missing {m_csv}"
    assert os.path.exists(fs_csv), f"Missing {fs_csv}"
    assert os.path.exists(shap_csv), f"Missing {shap_csv}"
    
    # 1. Validate Model Comparison Metrics
    m_df = pd.read_csv(m_csv)
    print(f"[CHECK 1] Validating model comparison table ({len(m_df)} models)...")
    for _, r in m_df.iterrows():
        m_name = r["model"]
        tp, tn, fp, fn = r["tp"], r["tn"], r["fp"], r["fn"]
        total = tp + tn + fp + fn
        
        assert total == 11729, f"Confusion matrix total mismatch for {m_name}: {total} != 11729"
        
        expected_acc = (tp + tn) / total
        expected_prec = tp / (tp + fp) if (tp + fp) > 0 else 0
        expected_rec = tp / (tp + fn) if (tp + fn) > 0 else 0
        expected_f1 = 2 * (expected_prec * expected_rec) / (expected_prec + expected_rec) if (expected_prec + expected_rec) > 0 else 0
        
        assert np.isclose(r["accuracy"], expected_acc, atol=1e-3), f"Accuracy mismatch in {m_name}"
        assert np.isclose(r["precision"], expected_prec, atol=1e-3), f"Precision mismatch in {m_name}"
        assert np.isclose(r["recall"], expected_rec, atol=1e-3), f"Recall mismatch in {m_name}"
        assert np.isclose(r["f1_score"], expected_f1, atol=1e-3), f"F1 mismatch in {m_name}"
        assert 0.0 <= r["roc_auc"] <= 1.0, f"ROC-AUC out of bounds in {m_name}"
        assert r["training_time_sec"] > 0, f"Invalid training time in {m_name}"
        assert r["inference_latency_ms_per_1k"] > 0, f"Invalid latency in {m_name}"
        
    print("  --> PASS: All model metrics are mathematically consistent with confusion matrix counts.")
    
    # 2. Validate Feature Selection Monotonicity / Feasibility
    fs_df = pd.read_csv(fs_csv)
    print(f"[CHECK 2] Validating feature selection results ({len(fs_df)} subsets)...")
    for _, r in fs_df.iterrows():
        assert 0.0 <= r["accuracy"] <= 1.0
        assert 0.0 <= r["f1_score"] <= 1.0
        assert 0.0 <= r["roc_auc"] <= 1.0
        assert r["feature_count"] > 0
    print("  --> PASS: Feature selection values validated.")
    
    # 3. Validate SHAP Feature Importance
    shap_df = pd.read_csv(shap_csv)
    print(f"[CHECK 3] Validating SHAP rankings ({len(shap_df)} features)...")
    assert not shap_df["mean_abs_shap"].isnull().any()
    assert (shap_df["mean_abs_shap"] >= 0).all()
    assert (shap_df["mean_abs_shap"].diff().dropna() <= 0).all(), "SHAP dataframe must be sorted in descending order"
    print("  --> PASS: SHAP global importance values strictly validated.")
    
    # 4. Validate Generated Figures
    print("[CHECK 4] Validating figure existence and non-zero byte size...")
    expected_figs = [
        "fig1_system_architecture.png", "fig1_system_architecture.pdf",
        "fig2_class_distribution.png", "fig2_class_distribution.pdf",
        "fig3_model_comparison.png", "fig3_model_comparison.pdf",
        "fig4_confusion_matrices.png", "fig4_confusion_matrices.pdf",
        "fig5_roc_pr_curves.png", "fig5_roc_pr_curves.pdf",
        "fig6_shap_feature_importance.png", "fig6_shap_feature_importance.pdf",
        "fig7_shap_summary_beeswarm.png", "fig7_shap_summary_beeswarm.pdf",
        "fig8_local_shap_explanation.png", "fig8_local_shap_explanation.pdf",
        "fig9_feature_reduction_comparison.png", "fig9_feature_reduction_comparison.pdf",
        "fig10_computational_comparison.png", "fig10_computational_comparison.pdf"
    ]
    for fig_name in expected_figs:
        p = os.path.join(fig_dir, fig_name)
        assert os.path.exists(p), f"Missing figure {fig_name}"
        assert os.path.getsize(p) > 1000, f"Corrupt/empty figure {fig_name}"
    print("  --> PASS: All 10 publication figures verified.")
    
    print("\n================ ALL SCIENTIFIC INTEGRITY CHECKS PASSED ================\n")
    return True

if __name__ == "__main__":
    from src.data_loader import load_config
    cfg = load_config()
    validate_all_results(cfg)
