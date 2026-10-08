import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

train_df = pd.read_csv("data/processed/train.csv")
test_df = pd.read_csv("data/processed/test.csv")
target_col = "phishing"

X_train_raw = train_df.drop(columns=[target_col])
y_train = train_df[target_col].values
X_test_raw = test_df.drop(columns=[target_col])
y_test = test_df[target_col].values

shap_df = pd.read_csv("results/explanations/shap_global_feature_importance.csv")

# 1. Evaluate CV on training set for k in [5, 10, 20, 30, full(98)]
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for k in [5, 10, 20, 30, 98]:
    feats = list(shap_df["feature"].iloc[:k])
    X_tr_k = X_train_raw[feats].values
    f1_folds = []
    acc_folds = []
    for train_idx, val_idx in cv.split(X_tr_k, y_train):
        m = XGBClassifier(
            n_estimators=100, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8,
            eval_metric="logloss", random_state=42, n_jobs=-1
        )
        m.fit(X_tr_k[train_idx], y_train[train_idx])
        pred = m.predict(X_tr_k[val_idx])
        acc_folds.append(accuracy_score(y_train[val_idx], pred))
        f1_folds.append(f1_score(y_train[val_idx], pred))
    print(f"k={k}: CV Acc = {np.mean(acc_folds)*100:.2f}% ± {np.std(acc_folds)*100:.2f}%, CV F1 = {np.mean(f1_folds)*100:.2f}% ± {np.std(f1_folds)*100:.2f}%")

# 2. Multi-seed evaluation for Top-20 on test set
top20_feats = list(shap_df["feature"].iloc[:20])
X_tr_20 = X_train_raw[top20_feats].values
X_te_20 = X_test_raw[top20_feats].values

seeds = [42, 123, 456, 789, 2024]
top20_accs = []
top20_f1s = []
top20_aucs = []

for s in seeds:
    m = XGBClassifier(
        n_estimators=100, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8,
        eval_metric="logloss", random_state=s, n_jobs=-1
    )
    m.fit(X_tr_20, y_train)
    pred = m.predict(X_te_20)
    prob = m.predict_proba(X_te_20)[:, 1]
    top20_accs.append(accuracy_score(y_test, pred))
    top20_f1s.append(f1_score(y_test, pred))
    top20_aucs.append(roc_auc_score(y_test, prob))
    print(f"Seed {s}: Acc={accuracy_score(y_test, pred)*100:.2f}%, F1={f1_score(y_test, pred)*100:.2f}%, AUC={roc_auc_score(y_test, prob):.4f}")

print(f"\nTop-20 5-Seed Test Mean:")
print(f"Accuracy: {np.mean(top20_accs)*100:.2f}% ± {np.std(top20_accs)*100:.2f}%")
print(f"F1: {np.mean(top20_f1s)*100:.2f}% ± {np.std(top20_f1s)*100:.2f}%")
print(f"ROC-AUC: {np.mean(top20_aucs):.4f} ± {np.std(top20_aucs):.4f}")
