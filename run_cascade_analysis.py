import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score

train_df = pd.read_csv("data/processed/train.csv")
test_df = pd.read_csv("data/processed/test.csv")
target_col = "phishing"

X_train_raw = train_df.drop(columns=[target_col])
y_train = train_df[target_col]
X_test_raw = test_df.drop(columns=[target_col])
y_test = test_df[target_col]

constant_features = [c for c in X_train_raw.columns if X_train_raw[c].var() == 0]
feature_cols = [c for c in X_train_raw.columns if c not in constant_features]

# Top 20 features:
shap_df = pd.read_csv("results/explanations/shap_global_feature_importance.csv")
top20_feats = list(shap_df["feature"].iloc[:20])

# Lexical 84 features:
net_feats = ['time_response', 'domain_spf', 'asn_ip', 'time_domain_activation', 'time_domain_expiration', 
             'qty_ip_resolved', 'qty_nameservers', 'qty_mx_servers', 'ttl_hostname', 'tls_ssl_certificate', 
             'qty_redirects', 'url_google_index', 'domain_google_index', 'url_shortened']
lex84_feats = [c for c in feature_cols if c not in net_feats]

# Train Tier 1 (Lexical-84)
xgb_tier1 = XGBClassifier(
    n_estimators=100, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8,
    eval_metric="logloss", random_state=42, n_jobs=-1
)
xgb_tier1.fit(X_train_raw[lex84_feats], y_train)

# Train Tier 2 (Top-20)
xgb_tier2 = XGBClassifier(
    n_estimators=100, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8,
    eval_metric="logloss", random_state=42, n_jobs=-1
)
xgb_tier2.fit(X_train_raw[top20_feats], y_train)

# Test evaluation
prob_tier1 = xgb_tier1.predict_proba(X_test_raw[lex84_feats])[:, 1]
tau_L, tau_H = 0.10, 0.90

# Tier 1 decisions
t1_legit = prob_tier1 < tau_L
t1_phish = prob_tier1 > tau_H
t1_deferred = (prob_tier1 >= tau_L) & (prob_tier1 <= tau_H)

print(f"Tier 1 resolved: {t1_legit.sum() + t1_phish.sum()} ({t1_legit.sum()} legit, {t1_phish.sum()} phish)")
print(f"Tier 1 deferred: {t1_deferred.sum()}")

# Leaks at Tier 1:
# A leak is phishing URL that Tier 1 declared legitimate (prob < 0.10)
phish_in_t1_legit = (y_test[t1_legit] == 1).sum()
total_t1_legit = t1_legit.sum()
print(f"Tier 1 phishing leaks: {phish_in_t1_legit} / {total_t1_legit} ({phish_in_t1_legit/total_t1_legit*100:.2f}%)")

# Pathless phishing in Tier 1:
pathless_mask = X_test_raw["directory_length"] == -1
pathless_phish = (pathless_mask) & (y_test == 1)
print(f"Total pathless phishing URLs: {pathless_phish.sum()}")
print(f"Pathless phishing URLs called legitimate at Tier 1: {(pathless_phish & t1_legit).sum()} ({(pathless_phish & t1_legit).sum() / pathless_phish.sum() * 100:.1f}%)")
print(f"Pathless phishing URLs deferred to Tier 2: {(pathless_phish & t1_deferred).sum()}")
print(f"Pathless phishing URLs called phishing at Tier 1: {(pathless_phish & t1_phish).sum()}")

# Tier 2 predictions on deferred
prob_tier2 = xgb_tier2.predict_proba(X_test_raw.loc[t1_deferred, top20_feats])[:, 1]
pred_tier2 = (prob_tier2 >= 0.5).astype(int)

# Combine end-to-end cascade predictions
y_cascade_pred = np.zeros(len(y_test), dtype=int)
y_cascade_pred[t1_phish] = 1
y_cascade_pred[t1_legit] = 0
y_cascade_pred[t1_deferred] = pred_tier2

# End-to-end confusion matrix
tn_c, fp_c, fn_c, tp_c = confusion_matrix(y_test, y_cascade_pred).ravel()
total_phish = (y_test == 1).sum() # 6129
total_legit = (y_test == 0).sum() # 5600

cascade_acc = (tp_c + tn_c) / len(y_test)
cascade_f1 = f1_score(y_test, y_cascade_pred)
cascade_fnr = fn_c / total_phish
cascade_fpr = fp_c / total_legit

print("\n--- CASCADE END-TO-END METRICS ---")
print(f"Total test: {len(y_test)}")
print(f"TN: {tn_c}, FP: {fp_c}, FN: {fn_c}, TP: {tp_c}")
print(f"Accuracy: {cascade_acc*100:.2f}%")
print(f"F1: {cascade_f1*100:.2f}%")
print(f"End-to-End FNR: {cascade_fnr*100:.2f}% (FN = {fn_c} / {total_phish})")
print(f"End-to-End FPR: {cascade_fpr*100:.2f}% (FP = {fp_c} / {total_legit})")

# Monolithic XGBoost metrics for comparison:
xgb_mono = XGBClassifier(
    n_estimators=100, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8,
    eval_metric="logloss", random_state=42, n_jobs=-1
)
xgb_mono.fit(X_train_raw[feature_cols], y_train)
y_mono_pred = xgb_mono.predict(X_test_raw[feature_cols])
tn_m, fp_m, fn_m, tp_m = confusion_matrix(y_test, y_mono_pred).ravel()
mono_fnr = fn_m / total_phish
mono_fpr = fp_m / total_legit
print("\n--- MONOLITHIC XGBOOST METRICS ---")
print(f"TN: {tn_m}, FP: {fp_m}, FN: {fn_m}, TP: {tp_m}")
print(f"Monolithic FNR: {mono_fnr*100:.2f}% (FN = {fn_m} / {total_phish})")
print(f"Monolithic FPR: {mono_fpr*100:.2f}% (FP = {fp_m} / {total_legit})")
