"""
Evaluation module: calculates scientific performance metrics and generates curve diagnostics.
"""

import time
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    roc_curve,
    precision_recall_curve
)

def evaluate_predictions(y_true, y_pred, y_prob=None):
    """
    Compute comprehensive scientific evaluation metrics.
    """
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0
    
    metrics = {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1_score": float(f1),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
        "fpr": float(fpr),
        "fnr": float(fnr)
    }
    
    if y_prob is not None:
        try:
            auc = roc_auc_score(y_true, y_prob)
            pr_auc = average_precision_score(y_true, y_prob)
            metrics["roc_auc"] = float(auc)
            metrics["pr_auc"] = float(pr_auc)
        except Exception:
            metrics["roc_auc"] = np.nan
            metrics["pr_auc"] = np.nan
    else:
        metrics["roc_auc"] = np.nan
        metrics["pr_auc"] = np.nan
        
    return metrics

def measure_inference_speed(model, X_sample, n_iterations=20):
    """
    Measure inference latency in milliseconds per 1,000 queries.
    Returns median, mean, and standard deviation across repeated iterations.
    """
    # Warm-up runs to stabilize CPU caches
    _ = model.predict(X_sample[:min(100, len(X_sample))])
    _ = model.predict(X_sample)
    
    latencies = []
    for _ in range(n_iterations):
        t0 = time.perf_counter()
        _ = model.predict(X_sample)
        t1 = time.perf_counter()
        total_time_sec = t1 - t0
        latency_per_1k_ms = (total_time_sec / len(X_sample)) * 1000.0 * 1000.0
        latencies.append(latency_per_1k_ms)
        
    return {
        "median_ms": float(np.median(latencies)),
        "mean_ms": float(np.mean(latencies)),
        "std_ms": float(np.std(latencies)),
        "raw": latencies
    }

