import numpy as np
import pandas as pd
from xgboost import XGBClassifier
import shap
from scipy.stats import spearmanr, kendalltau

train_df = pd.read_csv("data/processed/train.csv")
target_col = "phishing"

X_train_raw = train_df.drop(columns=[target_col])
y_train = train_df[target_col]

constant_features = [c for c in X_train_raw.columns if X_train_raw[c].var() == 0]
feature_cols = [c for c in X_train_raw.columns if c not in constant_features]
X_train = X_train_raw[feature_cols]

seeds = [42, 123, 456, 789, 2024]

# Case A: Model trained with seed 42, varying the 500-row explanation sample
model_42 = XGBClassifier(
    n_estimators=100, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8,
    eval_metric="logloss", random_state=42, n_jobs=-1
)
model_42.fit(X_train, y_train)
explainer_42 = shap.TreeExplainer(model_42)

shap_runs_sample_var = []
for s in seeds:
    idx = np.random.RandomState(s).choice(len(X_train), size=500, replace=False)
    X_exp = X_train.iloc[idx]
    sv = explainer_42(X_exp)
    vals = sv.values[:, :, 1] if len(sv.values.shape) == 3 else sv.values
    mean_abs = np.mean(np.abs(vals), axis=0)
    shap_runs_sample_var.append(mean_abs)

base_ranks_98 = np.argsort(-shap_runs_sample_var[0])
base_top20_idx = base_ranks_98[:20]

print("--- CASE A: Fixed Model, Varying 500-sample seed ---")
for i in range(1, len(seeds)):
    sp_98, _ = spearmanr(shap_runs_sample_var[0], shap_runs_sample_var[i])
    # For top 20 features:
    kt_20, _ = kendalltau(shap_runs_sample_var[0][base_top20_idx], shap_runs_sample_var[i][base_top20_idx])
    sp_20, _ = spearmanr(shap_runs_sample_var[0][base_top20_idx], shap_runs_sample_var[i][base_top20_idx])
    print(f"Seed {seeds[i]}: Spearman 98={sp_98:.4f}, Kendall tau Top-20={kt_20:.4f}, Spearman Top-20={sp_20:.4f}")

# Case B: Model retrained per seed, fixed 500-row sample (seed 42)
shap_runs_model_retrain = []
fixed_idx = np.random.RandomState(42).choice(len(X_train), size=500, replace=False)
X_exp_fixed = X_train.iloc[fixed_idx]

for s in seeds:
    m = XGBClassifier(
        n_estimators=100, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8,
        eval_metric="logloss", random_state=s, n_jobs=-1
    )
    m.fit(X_train, y_train)
    exp = shap.TreeExplainer(m)
    sv = exp(X_exp_fixed)
    vals = sv.values[:, :, 1] if len(sv.values.shape) == 3 else sv.values
    mean_abs = np.mean(np.abs(vals), axis=0)
    shap_runs_model_retrain.append(mean_abs)

print("\n--- CASE B: Model Retrained per Seed, Fixed Explanation Sample ---")
for i in range(1, len(seeds)):
    sp_98, _ = spearmanr(shap_runs_model_retrain[0], shap_runs_model_retrain[i])
    kt_20, _ = kendalltau(shap_runs_model_retrain[0][base_top20_idx], shap_runs_model_retrain[i][base_top20_idx])
    sp_20, _ = spearmanr(shap_runs_model_retrain[0][base_top20_idx], shap_runs_model_retrain[i][base_top20_idx])
    print(f"Seed {seeds[i]}: Spearman 98={sp_98:.4f}, Kendall tau Top-20={kt_20:.4f}, Spearman Top-20={sp_20:.4f}")

# Case C: Both Model Retrained and Explanation Sample varies per seed
shap_runs_both = []
for s in seeds:
    m = XGBClassifier(
        n_estimators=100, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8,
        eval_metric="logloss", random_state=s, n_jobs=-1
    )
    m.fit(X_train, y_train)
    exp = shap.TreeExplainer(m)
    idx = np.random.RandomState(s).choice(len(X_train), size=500, replace=False)
    sv = exp(X_train.iloc[idx])
    vals = sv.values[:, :, 1] if len(sv.values.shape) == 3 else sv.values
    mean_abs = np.mean(np.abs(vals), axis=0)
    shap_runs_both.append(mean_abs)

print("\n--- CASE C: Both Model Retrained and Explanation Sample Varies ---")
for i in range(1, len(seeds)):
    sp_98, _ = spearmanr(shap_runs_both[0], shap_runs_both[i])
    kt_20, _ = kendalltau(shap_runs_both[0][base_top20_idx], shap_runs_both[i][base_top20_idx])
    sp_20, _ = spearmanr(shap_runs_both[0][base_top20_idx], shap_runs_both[i][base_top20_idx])
    print(f"Seed {seeds[i]}: Spearman 98={sp_98:.4f}, Kendall tau Top-20={kt_20:.4f}, Spearman Top-20={sp_20:.4f}")
