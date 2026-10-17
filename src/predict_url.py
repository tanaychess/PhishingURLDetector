"""
Interactive Live Phishing URL Predictor & Explainability Tool.
Author: Tanay Samson Pathare (Bhonsala Military College)

Provides instant inference and SHAP local feature risk attribution for any URL sample.
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np
import shap
import xgboost as xgb
import yaml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data_loader import load_config
from src.feature_engineering import get_feature_descriptions

def run_prediction_demo(sample_index=0, model_type="xgboost"):
    """
    Load test data, perform live prediction with XGBoost, and generate instant SHAP explanation.
    """
    config = load_config()
    test_path = config["dataset"]["processed_test_path"]
    
    if not os.path.exists(test_path):
        print("Processed test set not found! Running master pipeline first...")
        from experiments.run_all import run_master_pipeline
        run_master_pipeline()
        
    test_df = pd.read_csv(test_path)
    target_col = config["dataset"]["target_column"]
    
    X_test = test_df.drop(columns=[target_col])
    y_test = test_df[target_col]
    
    # Bound sample index
    if sample_index < 0 or sample_index >= len(test_df):
        sample_index = np.random.randint(0, len(test_df))
        
    sample_x = X_test.iloc[[sample_index]]
    ground_truth = "PHISHING" if y_test.iloc[sample_index] == 1 else "LEGITIMATE"
    
    # Train/load XGBoost champion model
    train_path = config["dataset"]["processed_train_path"]
    train_df = pd.read_csv(train_path)
    X_train = train_df.drop(columns=[target_col])
    y_train = train_df[target_col]
    
    xgb_cfg = config["models"]["xgboost"]
    model = xgb.XGBClassifier(
        n_estimators=xgb_cfg.get("n_estimators", 100),
        max_depth=xgb_cfg.get("max_depth", 6),
        learning_rate=xgb_cfg.get("learning_rate", 0.1),
        subsample=xgb_cfg.get("subsample", 0.8),
        colsample_bytree=xgb_cfg.get("colsample_bytree", 0.8),
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1,
        tree_method="hist"
    )
    model.fit(X_train, y_train)
    
    # Inference
    pred_prob = float(model.predict_proba(sample_x)[0, 1])
    pred_label = "PHISHING" if pred_prob >= 0.5 else "LEGITIMATE"
    
    # TreeSHAP Local Attribution
    explainer = shap.TreeExplainer(model)
    shap_vals = explainer(sample_x)
    raw_shap = shap_vals.values[0]
    
    feature_names = list(X_test.columns)
    desc_dict = get_feature_descriptions()
    
    # Top 5 positive and negative contributors
    top_pos = np.argsort(raw_shap)[-5:][::-1]
    top_neg = np.argsort(raw_shap)[:5]
    
    print("\n" + "=" * 78)
    print("      EXPLAINABLE PHISHING DETECTION: LIVE INFERENCE & EXPLANATION")
    print("      Author: Tanay Samson Pathare (Bhonsala Military College)")
    print("=" * 78)
    print(f"\n[QUERY SAMPLE #{sample_index}]")
    print(f"  * Ground Truth Label   : {ground_truth}")
    print(f"  * Model Classification : {pred_label}")
    print(f"  * Phishing Probability : {pred_prob * 100:.2f}%")
    print(f"  * Verdict Status       : {'[MATCH / CORRECT]' if pred_label == ground_truth else '[MISMATCH]'}")
    
    print("\n" + "-" * 78)
    print("  TOP PHISHING RISK FACTORS (Positive SHAP Force -> Pushing to Phishing):")
    print("-" * 78)
    print(f"  {'Rank':<4} {'Feature Name':<26} {'Value':<10} {'SHAP Impact':<12} {'Description'}")
    print(f"  {'-'*4} {'-'*26} {'-'*10} {'-'*12} {'-'*22}")
    for rank, idx in enumerate(top_pos, 1):
        f_name = feature_names[idx]
        val = float(sample_x.iloc[0, idx])
        s_val = float(raw_shap[idx])
        desc = desc_dict.get(f_name, "Structural URL characteristic")
        if s_val > 0.001:
            print(f"   {rank:<3} {f_name:<26} {val:<10.1f} {f'+{s_val:.4f}':<12} {desc}")
            
    print("\n" + "-" * 78)
    print("  TOP LEGITIMATE BENIGN SIGNALS (Negative SHAP Force -> Pushing to Benign):")
    print("-" * 78)
    print(f"  {'Rank':<4} {'Feature Name':<26} {'Value':<10} {'SHAP Impact':<12} {'Description'}")
    print(f"  {'-'*4} {'-'*26} {'-'*10} {'-'*12} {'-'*22}")
    for rank, idx in enumerate(top_neg, 1):
        f_name = feature_names[idx]
        val = float(sample_x.iloc[0, idx])
        s_val = float(raw_shap[idx])
        desc = desc_dict.get(f_name, "Structural URL characteristic")
        if s_val < -0.001:
            print(f"   {rank:<3} {f_name:<26} {val:<10.1f} {f'{s_val:.4f}':<12} {desc}")
            
    print("\n" + "=" * 78 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Explainable Phishing URL Predictor")
    parser.add_argument("--sample", type=int, default=0, help="Test sample index (0 to 11728)")
    args = parser.parse_args()
    run_prediction_demo(sample_index=args.sample)
