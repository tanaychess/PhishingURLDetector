"""
Feature selection module: evaluates model performance and computational efficiency across reduced SHAP feature subsets.
"""

import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from src.evaluate import evaluate_predictions, measure_inference_speed

def run_feature_selection_experiments(X_train_df, y_train, X_test_df, y_test, global_importance_df, config, trained_full_model=None, full_latency_stats=None):
    """
    Train and evaluate models on Full (98), Top 30, Top 20, Top 10, and Top 5 feature subsets.
    Feature rankings are derived exclusively from training set TreeSHAP importance to eliminate selection leakage.
    Ensures Full (98) metrics identically match baseline XGBoost benchmarks.
    """
    print("\n================ STARTING FEATURE SELECTION BENCHMARKING ================")
    
    network_keywords = ['time_', 'ttl_', 'asn_', 'qty_redirect', 'nameservers', 'mx_servers', 'ip_resolved', 'tls_', 'ssl_', 'spf', 'google_index', 'shortened']
    
    ranked_features = global_importance_df["feature"].tolist()
    total_features = len(ranked_features)
    subsets = [total_features, 30, 20, 10, 5]
    
    results = []
    subset_models = {}
    subset_latencies = {}
    seed = config["project"]["random_seed"]
    out_dir = config["paths"]["results_metrics"]
    fig_dir = config["paths"]["figures"]
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    
    xgb_cfg = config["models"]["xgboost"]
    
    for k in subsets:
        current_k = min(k, total_features)
        selected_features = ranked_features[:current_k]
        
        subset_name = f"Full ({current_k} feats)" if current_k == total_features else f"Top-{current_k}"
        print(f"\n>>> Evaluating Feature Subset: {subset_name}...")
        
        # Count network vs lexical
        net_count = sum(1 for f in selected_features if any(nk in f.lower() for nk in network_keywords))
        lex_count = current_k - net_count
        
        if current_k == total_features and trained_full_model is not None:
            # Reuse full model to ensure exact 100% metric synchronization
            model = trained_full_model
            selected_features = list(X_train_df.columns)
            X_tr_sub = X_train_df
            X_te_sub = X_test_df
            train_time_sec = 0.0 # already trained
            y_pred = model.predict(X_te_sub)
            y_prob = model.predict_proba(X_te_sub)[:, 1]
            if full_latency_stats is not None:
                lat_stats = full_latency_stats
            else:
                lat_stats = measure_inference_speed(model, X_te_sub, n_iterations=20)
        else:
            X_tr_sub = X_train_df[selected_features]
            X_te_sub = X_test_df[selected_features]
            
            model = xgb.XGBClassifier(
                n_estimators=xgb_cfg.get("n_estimators", 100),
                max_depth=xgb_cfg.get("max_depth", 6),
                learning_rate=xgb_cfg.get("learning_rate", 0.1),
                subsample=xgb_cfg.get("subsample", 0.8),
                colsample_bytree=xgb_cfg.get("colsample_bytree", 0.8),
                eval_metric="logloss",
                random_state=seed,
                n_jobs=-1,
                tree_method="hist"
            )
            t_start = time.perf_counter()
            model.fit(X_tr_sub, y_train)
            train_time_sec = time.perf_counter() - t_start
            
            y_pred = model.predict(X_te_sub)
            y_prob = model.predict_proba(X_te_sub)[:, 1]
            lat_stats = measure_inference_speed(model, X_te_sub, n_iterations=20)
            
        subset_models[subset_name] = (model, selected_features)
        subset_latencies[subset_name] = lat_stats
        
        # Evaluate Metrics
        metrics = evaluate_predictions(y_test, y_pred, y_prob)
        metrics["subset_name"] = subset_name
        metrics["feature_count"] = current_k
        metrics["network_features"] = net_count
        metrics["lexical_features"] = lex_count
        metrics["training_time_sec"] = round(train_time_sec, 4)
        metrics["inference_latency_ms_per_1k"] = round(lat_stats["median_ms"], 3)
        metrics["inference_latency_mean_ms"] = round(lat_stats["mean_ms"], 3)
        metrics["inference_latency_std_ms"] = round(lat_stats["std_ms"], 3)
        metrics["retention_ratio"] = round(current_k / total_features, 4)
        
        results.append(metrics)
        print(f"    Subset: {subset_name:<15} (Net: {net_count}, Lex: {lex_count}) | Acc: {metrics['accuracy']*100:.2f}% | F1: {metrics['f1_score']*100:.2f}% | ROC-AUC: {metrics['roc_auc']:.4f} | Latency: {metrics['inference_latency_ms_per_1k']:.2f}ms (mean {metrics['inference_latency_mean_ms']:.2f} ± {metrics['inference_latency_std_ms']:.2f})")
        
    fs_df = pd.DataFrame(results)
    csv_path = os.path.join(out_dir, "feature_selection_results.csv")
    fs_df.to_csv(csv_path, index=False)
    print(f"\nSaved feature selection results to {csv_path}")
    
    # Generate Feature Reduction Trade-Off Plot (Figure 9)
    fig, ax1 = plt.subplots(figsize=(8.5, 4.8), dpi=300)
    
    color1 = "#2980b9"
    color2 = "#27ae60"
    color3 = "#c0392b"
    
    x_labels = [r["subset_name"] for r in results]
    f1_scores = [r["f1_score"] * 100 for r in results]
    acc_scores = [r["accuracy"] * 100 for r in results]
    latencies = [r["inference_latency_ms_per_1k"] for r in results]
    
    x_idx = np.arange(len(x_labels))
    width = 0.30
    
    rects1 = ax1.bar(x_idx - width/2, acc_scores, width, label="Accuracy (%)", color=color1, alpha=0.9, edgecolor="black")
    rects2 = ax1.bar(x_idx + width/2, f1_scores, width, label="F1-Score (%)", color=color2, alpha=0.9, edgecolor="black")
    
    ax1.set_xlabel("Feature Dimension Subset", fontsize=10.5, fontweight="bold")
    ax1.set_ylabel("Classification Metric Score (%)", fontsize=10.5, fontweight="bold")
    ax1.set_xticks(x_idx)
    ax1.set_xticklabels(x_labels, fontsize=9.5, fontweight="bold")
    ax1.set_ylim(88, 100)
    ax1.set_yticks([88, 90, 92, 94, 96, 98, 100])
    ax1.grid(True, linestyle="--", alpha=0.35, axis="y")
    
    # Value annotations on bars
    for rect in rects1:
        h = rect.get_height()
        ax1.annotate(f"{h:.2f}%",
                     xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(-1, 3),
                     textcoords="offset points",
                     ha="center", va="bottom", fontsize=6.8, fontweight="bold", color=color1)
    for rect in rects2:
        h = rect.get_height()
        ax1.annotate(f"{h:.2f}%",
                     xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(1, 3),
                     textcoords="offset points",
                     ha="center", va="bottom", fontsize=6.8, fontweight="bold", color=color2)
    
    # Secondary axis for inference latency
    ax2 = ax1.twinx()
    line = ax2.plot(x_idx, latencies, color=color3, marker="s", linewidth=2.0, markersize=6.5, label="Inference Latency (ms / 1k queries)")
    ax2.set_ylabel("Inference Latency (ms / 1,000 queries)", color=color3, fontsize=10.5, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor=color3)
    ax2.set_ylim(0.8, 3.2)
    ax2.set_yticks([1.0, 1.5, 2.0, 2.5, 3.0])
    
    # Value annotations for latency
    for i, lat in enumerate(latencies):
        ax2.annotate(f"{lat:.2f} ms",
                     xy=(x_idx[i], lat),
                     xytext=(0, 6),
                     textcoords="offset points",
                     ha="center", va="bottom", fontsize=7.5, color=color3, fontweight="bold",
                     bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor=color3, alpha=0.9, lw=0.7))
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", framealpha=0.92, fontsize=8.2)
    
    plt.title("Classification Performance vs. Dimensionality & Inference Latency", fontsize=11, fontweight="bold", pad=10)
    plt.tight_layout()
    
    fig_path = os.path.join(fig_dir, "fig9_feature_reduction_comparison.png")
    fig_pdf = os.path.join(fig_dir, "fig9_feature_reduction_comparison.pdf")
    plt.savefig(fig_path, dpi=300)
    plt.savefig(fig_pdf)
    plt.close()
    print(f"Saved feature reduction comparison figure to {fig_path}")
    
    return fs_df, subset_models, subset_latencies


