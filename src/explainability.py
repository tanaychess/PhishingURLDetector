"""
Explainability module: implements TreeSHAP analysis, global feature ranking, and local URL explanations.
"""

import os
import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_shap_analysis(model, X_train_df, X_test_df, y_test, config, feature_names):
    """
    Execute complete SHAP explainability pipeline.
    Global feature importance ranking is derived STRICTLY from the training set to prevent data leakage.
    Local explanations are generated for representative test instances.
    """
    print("\n================ STARTING SHAP EXPLAINABILITY ANALYSIS ================")
    
    n_samples = config["explainability"].get("test_explanation_samples", 500)
    out_exp_dir = config["paths"]["results_explanations"]
    fig_dir = config["paths"]["figures"]
    os.makedirs(out_exp_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    
    # 1. Global Importance: Computed strictly on TRAINING partition to prevent selection leakage
    train_sample_indices = np.random.RandomState(config["project"]["random_seed"]).choice(
        len(X_train_df), size=min(n_samples, len(X_train_df)), replace=False
    )
    X_train_explain = X_train_df.iloc[train_sample_indices]
    
    print(">>> Initializing TreeSHAP Explainer on Training Data...")
    explainer = shap.TreeExplainer(model)
    train_shap_values = explainer(X_train_explain)
    
    if len(train_shap_values.values.shape) == 3:
        train_raw_shap_vals = train_shap_values.values[:, :, 1]
    else:
        train_raw_shap_vals = train_shap_values.values
        
    mean_abs_shap = np.mean(np.abs(train_raw_shap_vals), axis=0)
    global_importance_df = pd.DataFrame({
        "feature": feature_names,
        "mean_abs_shap": mean_abs_shap
    }).sort_values(by="mean_abs_shap", ascending=False).reset_index(drop=True)
    
    global_importance_df["rank"] = np.arange(1, len(global_importance_df) + 1)
    
    # Save global ranking CSV
    global_csv_path = os.path.join(out_exp_dir, "shap_global_feature_importance.csv")
    global_importance_df.to_csv(global_csv_path, index=False)
    print(f"Saved global SHAP importance (derived from training data) to {global_csv_path}")
    print("\nTop 15 Most Influential Phishing Features by SHAP (Training Set):")
    for idx, row in global_importance_df.head(15).iterrows():
        print(f"  {row['rank']:2d}. {row['feature']:<28} : {row['mean_abs_shap']:.5f}")
        
    # 2. Generate and Save Global SHAP Summary Figures
    # A) Global Feature Importance Bar Plot
    plt.figure(figsize=(9, 6), dpi=300)
    top_20 = global_importance_df.head(20)
    sns.barplot(
        data=top_20,
        x="mean_abs_shap",
        y="feature",
        palette="viridis",
        hue="feature",
        legend=False
    )
    plt.title("Top 20 Most Influential Features (Mean |SHAP Value| on Training Set)", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Mean |SHAP Value| (Impact on Model Log-Odds)", fontsize=11)
    plt.ylabel("URL / Network Feature", fontsize=11)
    plt.tight_layout()
    bar_fig_path = os.path.join(fig_dir, "fig6_shap_feature_importance.png")
    bar_fig_pdf = os.path.join(fig_dir, "fig6_shap_feature_importance.pdf")
    plt.savefig(bar_fig_path, dpi=300)
    plt.savefig(bar_fig_pdf)
    plt.close()
    print(f"Saved SHAP bar plot to {bar_fig_path}")
    
    # B) Beeswarm Summary Plot (computed on training explanation sample)
    plt.figure(figsize=(10, 7), dpi=300)
    shap.summary_plot(
        train_raw_shap_vals,
        X_train_explain,
        feature_names=feature_names,
        max_display=15,
        show=False
    )
    plt.title("SHAP Summary Beeswarm Plot: Feature Impact on Log-Odds", fontsize=12, fontweight="bold", pad=14)
    plt.tight_layout()
    beeswarm_path = os.path.join(fig_dir, "fig7_shap_summary_beeswarm.png")
    beeswarm_pdf = os.path.join(fig_dir, "fig7_shap_summary_beeswarm.pdf")
    plt.savefig(beeswarm_path, dpi=300)
    plt.savefig(beeswarm_pdf)
    plt.close()
    print(f"Saved SHAP beeswarm plot to {beeswarm_path}")
    
    # 3. Local Explanations for Representative Test Samples
    print(">>> Generating Local Instance Explanations on Test Samples...")
    test_sample_indices = np.random.RandomState(config["project"]["random_seed"]).choice(
        len(X_test_df), size=min(n_samples, len(X_test_df)), replace=False
    )
    X_test_explain = X_test_df.iloc[test_sample_indices]
    y_test_explain = y_test.iloc[test_sample_indices]
    
    test_shap_values = explainer(X_test_explain)
    if len(test_shap_values.values.shape) == 3:
        test_raw_shap_vals = test_shap_values.values[:, :, 1]
    else:
        test_raw_shap_vals = test_shap_values.values
        
    local_indices = config["explainability"].get("local_explanation_indices", [0, 5, 12, 42])
    local_records = []
    
    for idx in local_indices:
        if idx >= len(X_test_explain):
            idx = 0
        sample_feat = X_test_explain.iloc[idx]
        sample_y_true = int(y_test_explain.iloc[idx])
        sample_pred = int(model.predict(X_test_explain.iloc[[idx]])[0])
        sample_prob = float(model.predict_proba(X_test_explain.iloc[[idx]])[0, 1])
        
        sample_shap = test_raw_shap_vals[idx]
        
        top_pos_idx = np.argsort(sample_shap)[-5:][::-1]
        top_neg_idx = np.argsort(sample_shap)[:5]
        
        for p_idx in top_pos_idx:
            local_records.append({
                "sample_id": idx,
                "ground_truth": "Phishing" if sample_y_true == 1 else "Legitimate",
                "predicted_label": "Phishing" if sample_pred == 1 else "Legitimate",
                "phishing_probability": round(sample_prob, 4),
                "feature": feature_names[p_idx],
                "feature_value": float(sample_feat.iloc[p_idx]),
                "shap_value": round(float(sample_shap[p_idx]), 5),
                "contribution_direction": "Increases Phishing Risk"
            })
            
        for n_idx in top_neg_idx:
            local_records.append({
                "sample_id": idx,
                "ground_truth": "Phishing" if sample_y_true == 1 else "Legitimate",
                "predicted_label": "Phishing" if sample_pred == 1 else "Legitimate",
                "phishing_probability": round(sample_prob, 4),
                "feature": feature_names[n_idx],
                "feature_value": float(sample_feat.iloc[n_idx]),
                "shap_value": round(float(sample_shap[n_idx]), 5),
                "contribution_direction": "Decreases Phishing Risk (Legitimate Signal)"
            })
            
    local_df = pd.DataFrame(local_records)
    local_csv_path = os.path.join(out_exp_dir, "local_explanations.csv")
    local_df.to_csv(local_csv_path, index=False)
    print(f"Saved local instance explanations to {local_csv_path}")
    
    # Generate local explanation plot for test sample 0
    sample_0_shap = test_raw_shap_vals[0]
    top_contrib_indices = np.argsort(np.abs(sample_0_shap))[-10:][::-1]
    
    plt.figure(figsize=(9, 5), dpi=300)
    contrib_features = [feature_names[i] for i in top_contrib_indices]
    contrib_values = [sample_0_shap[i] for i in top_contrib_indices]
    colors = ["#e74c3c" if val > 0 else "#2ecc71" for val in contrib_values]
    
    y_pos = np.arange(len(contrib_features))
    plt.barh(y_pos, contrib_values, color=colors, align="center", edgecolor="black", alpha=0.85)
    plt.yticks(y_pos, contrib_features, fontsize=10)
    plt.gca().invert_yaxis()
    plt.axvline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.xlabel("SHAP Value (Contribution to Model Output)", fontsize=11)
    
    s0_label = "Phishing" if y_test_explain.iloc[0] == 1 else "Legitimate"
    s0_prob = model.predict_proba(X_test_explain.iloc[[0]])[0, 1]
    plt.title(f"Local Instance Explanation (True: {s0_label}, P(Phishing) = {s0_prob:.3f})", fontsize=11, fontweight="bold", pad=12)
    plt.tight_layout()
    local_fig_path = os.path.join(fig_dir, "fig8_local_shap_explanation.png")
    local_fig_pdf = os.path.join(fig_dir, "fig8_local_shap_explanation.pdf")
    plt.savefig(local_fig_path, dpi=300)
    plt.savefig(local_fig_pdf)
    plt.close()
    print(f"Saved local explanation figure to {local_fig_path}")
    
    return global_importance_df, local_df

