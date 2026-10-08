"""
Computational efficiency benchmarking module: measures runtime latency, model memory footprints, and resource overhead.
"""

import os
import sys
import time
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.evaluate import measure_inference_speed

def benchmark_computational_resources(trained_models, X_test_df, config, subset_models=None, model_latencies=None, subset_latencies=None):
    """
    Profile training runtime, inference latency, and serialized model size on disk for full and reduced models.
    Reuses standardized latency measurements to ensure 100% numerical consistency across all tables.
    """
    print("\n================ STARTING COMPUTATIONAL PROFILING ================")
    
    records = []
    out_dir = config["paths"]["results_metrics"]
    fig_dir = config["paths"]["figures"]
    temp_dir = "results/logs/temp_models"
    os.makedirs(temp_dir, exist_ok=True)
    
    # 1. Profile Full Baseline Models
    for name, model in trained_models.items():
        model_file = os.path.join(temp_dir, f"{name.replace(' ', '_').lower()}.joblib")
        joblib.dump(model, model_file, compress=3)
        size_mb = os.path.getsize(model_file) / (1024 * 1024)
        
        # Use existing latency stats if available, else measure
        if model_latencies and name in model_latencies:
            lat_stats = model_latencies[name]
        else:
            lat_stats = measure_inference_speed(model, X_test_df, n_iterations=20)
            
        median_latency = lat_stats["median_ms"]
        throughput_qps = float(1000.0 / (median_latency / 1000.0))
        
        records.append({
            "model": name,
            "feature_set": "Full (98)",
            "model_size_mb": round(size_mb, 4),
            "inference_latency_ms_per_1k": round(median_latency, 3),
            "inference_latency_mean_ms": round(lat_stats["mean_ms"], 3),
            "inference_latency_std_ms": round(lat_stats["std_ms"], 3),
            "throughput_queries_per_sec": round(throughput_qps, 1)
        })
        print(f"  {name:<22} | Size: {size_mb:6.3f} MB | Latency (1k): {median_latency:6.3f} ms (mean {lat_stats['mean_ms']:.3f} ± {lat_stats['std_ms']:.3f}) | Throughput: {throughput_qps:8.1f} q/s")
        
    # 2. Profile Top-20 XGBoost Model if provided
    if subset_models and "Top-20" in subset_models:
        top20_model, top20_feats = subset_models["Top-20"]
        top20_file = os.path.join(temp_dir, "xgboost_top20.joblib")
        joblib.dump(top20_model, top20_file, compress=3)
        top20_size_mb = os.path.getsize(top20_file) / (1024 * 1024)
        
        X_test_top20 = X_test_df[top20_feats]
        if subset_latencies and "Top-20" in subset_latencies:
            top20_lat_stats = subset_latencies["Top-20"]
        else:
            top20_lat_stats = measure_inference_speed(top20_model, X_test_top20, n_iterations=20)
            
        top20_median_lat = top20_lat_stats["median_ms"]
        top20_throughput = float(1000.0 / (top20_median_lat / 1000.0))
        
        records.append({
            "model": "XGBoost (Top-20)",
            "feature_set": "Top-20",
            "model_size_mb": round(top20_size_mb, 4),
            "inference_latency_ms_per_1k": round(top20_median_lat, 3),
            "inference_latency_mean_ms": round(top20_lat_stats["mean_ms"], 3),
            "inference_latency_std_ms": round(top20_lat_stats["std_ms"], 3),
            "throughput_queries_per_sec": round(top20_throughput, 1)
        })
        print(f"  {'XGBoost (Top-20)':<22} | Size: {top20_size_mb:6.3f} MB | Latency (1k): {top20_median_lat:6.3f} ms (mean {top20_lat_stats['mean_ms']:.3f} ± {top20_lat_stats['std_ms']:.3f}) | Throughput: {top20_throughput:8.1f} q/s")
        
    comp_df = pd.DataFrame(records)
    csv_path = os.path.join(out_dir, "computational_benchmarks.csv")
    comp_df.to_csv(csv_path, index=False)
    print(f"\nSaved computational benchmarks to {csv_path}")
    
    # Generate Computational Comparison Figure (Figure 10)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)
    
    # Latency Plot
    sns.barplot(data=comp_df, x="model", y="inference_latency_ms_per_1k", palette="mako", ax=ax1, edgecolor="black")
    ax1.set_title("Inference Latency (ms / 1k Queries)", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Latency (ms / 1,000 URLs)", fontsize=10, fontweight="bold")
    ax1.set_xlabel("Evaluated Model Architecture", fontsize=10, fontweight="bold")
    ax1.tick_params(axis="x", rotation=25)
    ax1.grid(True, linestyle="--", alpha=0.4, axis="y")
    for p in ax1.patches:
        h = p.get_height()
        if h > 0:
            ax1.annotate(f"{h:.2f} ms",
                         xy=(p.get_x() + p.get_width()/2, h),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha="center", va="bottom", fontsize=8, fontweight="bold")
    
    # Model Size Plot
    sns.barplot(data=comp_df, x="model", y="model_size_mb", palette="rocket", ax=ax2, edgecolor="black")
    ax2.set_title("Serialized Model Storage Footprint (MB)", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Serialized Size (MB)", fontsize=10, fontweight="bold")
    ax2.set_xlabel("Evaluated Model Architecture", fontsize=10, fontweight="bold")
    ax2.tick_params(axis="x", rotation=25)
    ax2.grid(True, linestyle="--", alpha=0.4, axis="y")
    for p in ax2.patches:
        h = p.get_height()
        if h > 0:
            ax2.annotate(f"{h:.3f} MB",
                         xy=(p.get_x() + p.get_width()/2, h),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha="center", va="bottom", fontsize=8, fontweight="bold")
    
    plt.tight_layout()
    fig_path = os.path.join(fig_dir, "fig10_computational_comparison.png")
    fig_pdf = os.path.join(fig_dir, "fig10_computational_comparison.pdf")
    plt.savefig(fig_path, dpi=300)
    plt.savefig(fig_pdf)
    plt.close()
    print(f"Saved computational figure to {fig_path}")
    
    return comp_df


