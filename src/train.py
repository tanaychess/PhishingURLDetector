"""
Training orchestrator module: executes model training, cross-validation, and metrics logging.
"""

import time
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from src.models import get_models
from src.evaluate import evaluate_predictions, measure_inference_speed

def train_and_evaluate_all(X_train, y_train, X_test, y_test, config, feature_names=None):
    """
    Train all configured models, perform 5-fold CV on training data, and evaluate on test set.
    """
    models = get_models(config)
    seed = config["project"]["random_seed"]
    n_folds = config["evaluation"].get("cross_validation_folds", 5)
    
    cv = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed)
    
    results = []
    trained_models = {}
    test_predictions = {}
    test_probabilities = {}
    latency_records = {}
    
    print(f"\n================ STARTING MODEL BENCHMARKING ({len(models)} Models) ================")
    
    for name, model in models.items():
        print(f"\n>>> Training and Evaluating: {name}...")
        
        # 1. 5-Fold Cross Validation on Training Partition
        cv_scoring = {
            "acc": "accuracy",
            "prec": "precision",
            "rec": "recall",
            "f1": "f1",
            "roc_auc": "roc_auc"
        }
        cv_res = cross_validate(model, X_train, y_train, cv=cv, scoring=cv_scoring, n_jobs=-1)
        cv_acc_mean = float(np.mean(cv_res["test_acc"]))
        cv_acc_std = float(np.std(cv_res["test_acc"]))
        cv_prec_mean = float(np.mean(cv_res["test_prec"]))
        cv_prec_std = float(np.std(cv_res["test_prec"]))
        cv_rec_mean = float(np.mean(cv_res["test_rec"]))
        cv_rec_std = float(np.std(cv_res["test_rec"]))
        cv_f1_mean = float(np.mean(cv_res["test_f1"]))
        cv_f1_std = float(np.std(cv_res["test_f1"]))
        cv_auc_mean = float(np.mean(cv_res["test_roc_auc"]))
        cv_auc_std = float(np.std(cv_res["test_roc_auc"]))
        
        # 2. Fit on full training set and measure training time
        t_start = time.perf_counter()
        model.fit(X_train, y_train)
        t_train_sec = time.perf_counter() - t_start
        
        # 3. Test Set Inference
        y_pred = model.predict(X_test)
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:, 1]
        elif hasattr(model, "decision_function"):
            dec = model.decision_function(X_test)
            y_prob = (dec - dec.min()) / (dec.max() - dec.min() + 1e-8)
        else:
            y_prob = None
            
        # 4. Measure Inference Latency with 2 warm-ups and 20 repeated runs
        latency_stats = measure_inference_speed(model, X_test, n_iterations=20)
        latency_records[name] = latency_stats
        
        # 5. Compute Detailed Test Metrics
        metrics = evaluate_predictions(y_test, y_pred, y_prob)
        metrics["model"] = name
        metrics["training_time_sec"] = round(t_train_sec, 4)
        metrics["inference_latency_ms_per_1k"] = round(latency_stats["median_ms"], 3)
        metrics["inference_latency_mean_ms"] = round(latency_stats["mean_ms"], 3)
        metrics["inference_latency_std_ms"] = round(latency_stats["std_ms"], 3)
        
        metrics["cv_accuracy_mean"] = round(cv_acc_mean, 4)
        metrics["cv_accuracy_std"] = round(cv_acc_std, 4)
        metrics["cv_precision_mean"] = round(cv_prec_mean, 4)
        metrics["cv_precision_std"] = round(cv_prec_std, 4)
        metrics["cv_recall_mean"] = round(cv_rec_mean, 4)
        metrics["cv_recall_std"] = round(cv_rec_std, 4)
        metrics["cv_f1_mean"] = round(cv_f1_mean, 4)
        metrics["cv_f1_std"] = round(cv_f1_std, 4)
        metrics["cv_auc_mean"] = round(cv_auc_mean, 4)
        metrics["cv_auc_std"] = round(cv_auc_std, 4)
        
        results.append(metrics)
        trained_models[name] = model
        test_predictions[name] = y_pred
        if y_prob is not None:
            test_probabilities[name] = y_prob
            
        print(f"    Test Acc: {metrics['accuracy']*100:.2f}% | F1: {metrics['f1_score']*100:.2f}% | ROC-AUC: {metrics['roc_auc']:.4f}")
        print(f"    CV F1: {metrics['cv_f1_mean']*100:.2f}% ± {metrics['cv_f1_std']*100:.2f}% | Train Time: {metrics['training_time_sec']:.2f}s")
        print(f"    Latency (per 1k queries): {metrics['inference_latency_ms_per_1k']:.2f} ms (mean {metrics['inference_latency_mean_ms']:.2f} ± {metrics['inference_latency_std_ms']:.2f})")
        
    results_df = pd.DataFrame(results)
    
    # Save results
    out_dir = config["paths"]["results_metrics"]
    os.makedirs(out_dir, exist_ok=True)
    results_df.to_csv(os.path.join(out_dir, "model_comparison.csv"), index=False)
    
    # Save predictions
    pred_dir = config["paths"]["results_predictions"]
    os.makedirs(pred_dir, exist_ok=True)
    preds_df = pd.DataFrame({"y_true": y_test})
    for m_name in test_predictions:
        preds_df[f"{m_name}_pred"] = test_predictions[m_name]
        if m_name in test_probabilities:
            preds_df[f"{m_name}_prob"] = test_probabilities[m_name]
    preds_df.to_csv(os.path.join(pred_dir, "test_predictions.csv"), index=False)
    
    print("\n================ BENCHMARKING COMPLETE ================")
    return results_df, trained_models, test_predictions, test_probabilities, latency_records


