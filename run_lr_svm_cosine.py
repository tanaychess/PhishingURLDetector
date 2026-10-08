import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import StandardScaler
from numpy.linalg import norm

train_df = pd.read_csv("data/processed/train.csv")
target_col = "phishing"

X_train_raw = train_df.drop(columns=[target_col])
y_train = train_df[target_col]

constant_features = [c for c in X_train_raw.columns if X_train_raw[c].var() == 0]
feature_cols = [c for c in X_train_raw.columns if c not in constant_features]
X_train = X_train_raw[feature_cols]

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Fit Logistic Regression
lr = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
lr.fit(X_train_scaled, y_train)

# Fit LinearSVC
svm = LinearSVC(C=1.0, max_iter=2000, random_state=42)
svm.fit(X_train_scaled, y_train)

# Coefficients
w_lr = lr.coef_.ravel()
w_svm = svm.coef_.ravel()

# Cosine similarity
cos_sim = np.dot(w_lr, w_svm) / (norm(w_lr) * norm(w_svm))
print(f"LR and Linear SVM Coefficient Cosine Similarity: {cos_sim:.4f}")
print(f"Norm of LR weights: {norm(w_lr):.4f}")
print(f"Norm of SVM weights: {norm(w_svm):.4f}")
