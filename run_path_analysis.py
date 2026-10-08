import os
import yaml
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

train_df = pd.read_csv("data/processed/train.csv")
test_df = pd.read_csv("data/processed/test.csv")
target_col = "phishing"

X_train_raw = train_df.drop(columns=[target_col])
y_train = train_df[target_col]
X_test_raw = test_df.drop(columns=[target_col])
y_test = test_df[target_col]

constant_features = [c for c in X_train_raw.columns if X_train_raw[c].var() == 0]
feature_cols = [c for c in X_train_raw.columns if c not in constant_features]
X_train = X_train_raw[feature_cols]
X_test = X_test_raw[feature_cols]

# Train XGBoost
xgb = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1
)
xgb.fit(X_train, y_train)
y_pred = xgb.predict(X_test)
y_prob = xgb.predict_proba(X_test)[:, 1]

# Path-bearing definition:
# In the paper: "exploiting dataset sampling skew (97.70% of phishing vs 39.71% of legitimate URLs contain paths)"
# directory_length > -1
path_mask = X_test["directory_length"] > -1
pathless_mask = ~path_mask

print(f"Total test URLs: {len(X_test)}")
print(f"Path-bearing test URLs: {path_mask.sum()} (Phishing: {y_test[path_mask].sum()}, Legitimate: {(~y_test[path_mask].astype(bool)).sum()})")
print(f"Pathless test URLs: {pathless_mask.sum()} (Phishing: {y_test[pathless_mask].sum()}, Legitimate: {(~y_test[pathless_mask].astype(bool)).sum()})")

print("\n--- XGBoost FULL (98 features) ---")
print("Overall:")
print(f"Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
print(f"F1: {f1_score(y_test, y_pred)*100:.2f}%")
print("Confusion Matrix (TN, FP, FN, TP):", confusion_matrix(y_test, y_pred).ravel())

print("\nOn Path-bearing URLs:")
y_test_path = y_test[path_mask]
y_pred_path = y_pred[path_mask]
tn, fp, fn, tp = confusion_matrix(y_test_path, y_pred_path).ravel()
acc_path = accuracy_score(y_test_path, y_pred_path) * 100
rec_path = recall_score(y_test_path, y_pred_path) * 100
f1_path = f1_score(y_test_path, y_pred_path) * 100
print(f"Accuracy: {acc_path:.2f}%, Recall: {rec_path:.2f}%, F1: {f1_path:.2f}%")
print(f"TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")

print("\nOn Pathless URLs:")
y_test_pathless = y_test[pathless_mask]
y_pred_pathless = y_pred[pathless_mask]
tn0, fp0, fn0, tp0 = confusion_matrix(y_test_pathless, y_pred_pathless).ravel()
acc_pathless = accuracy_score(y_test_pathless, y_pred_pathless) * 100
rec_pathless = recall_score(y_test_pathless, y_pred_pathless) * 100
f1_pathless = f1_score(y_test_pathless, y_pred_pathless) * 100
print(f"Accuracy: {acc_pathless:.2f}%, Recall: {rec_pathless:.2f}%, F1: {f1_pathless:.2f}%")
print(f"TN: {tn0}, FP: {fp0}, FN: {fn0}, TP: {tp0}")

# Now let's check the ablation model:
# "removing all 56 path, directory, file, and parameter features yielded a 28-feature URL/domain lexical model"
# What were the 28 features?
lex_groups = [c for c in feature_cols if not (c.startswith("qty_") and ("directory" in c or "file" in c or "params" in c)) 
              and c not in ["directory_length", "file_length", "params_length", "tld_present_params", "qty_params"]
              and c not in ['time_response', 'domain_spf', 'asn_ip', 'time_domain_activation', 'time_domain_expiration', 
                            'qty_ip_resolved', 'qty_nameservers', 'qty_mx_servers', 'ttl_hostname', 'tls_ssl_certificate', 
                            'qty_redirects', 'url_google_index', 'domain_google_index', 'url_shortened']]
print(f"\n28-feature lexical count: {len(lex_groups)}")
print("Features:", lex_groups)

xgb_28 = XGBClassifier(
    n_estimators=100, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8,
    eval_metric="logloss", random_state=42, n_jobs=-1
)
xgb_28.fit(X_train[lex_groups], y_train)
y_pred_28 = xgb_28.predict(X_test[lex_groups])
print("\n--- XGBoost 28-feature (No path/file/query groups) ---")
print(f"Overall Accuracy: {accuracy_score(y_test, y_pred_28)*100:.2f}%, F1: {f1_score(y_test, y_pred_28)*100:.2f}%")
acc_p28 = accuracy_score(y_test[path_mask], y_pred_28[path_mask]) * 100
acc_pl28 = accuracy_score(y_test[pathless_mask], y_pred_28[pathless_mask]) * 100
print(f"On Path-bearing: {acc_p28:.2f}%")
print(f"On Pathless: {acc_pl28:.2f}%")
