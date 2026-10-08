import os
import yaml
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from scipy.stats import spearmanr, kendalltau
from sklearn.model_selection import StratifiedKFold

# Load config
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

train_df = pd.read_csv("data/processed/train.csv")
test_df = pd.read_csv("data/processed/test.csv")
target_col = "phishing"

X_train_raw = train_df.drop(columns=[target_col])
y_train = train_df[target_col]
X_test_raw = test_df.drop(columns=[target_col])
y_test = test_df[target_col]

# 1. Feature filtering
constant_features = [c for c in X_train_raw.columns if X_train_raw[c].var() == 0]
feature_cols = [c for c in X_train_raw.columns if c not in constant_features]
X_train = X_train_raw[feature_cols]
X_test = X_test_raw[feature_cols]

# Check Vrbančič et al. feature categorization
# In [11], Table 1 or paper categorizes features.
# Let's see all columns:
print("Total raw columns:", len(X_train_raw.columns))
print("Constant features (13):", constant_features)

# Let's inspect features with url_, domain_, directory_, file_, params_, etc.
prefix_counts = {}
for c in X_train_raw.columns:
    prefix = c.split("_")[0]
    prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1
print("Prefix counts:", prefix_counts)

# Let's check which features are classified as resolver/network in the project:
# In paper:
# Lexical groups:
# 1) URL Lexical: 20
# 2) Domain Structural: 21 (8 retained)
# 3) Directory/Path: 18
# 4) File-Level: 18
# 5) Query/Parameter: 20
# 6) Resolver/Network: 14 (14 retained)
# Total = 20 + 21 + 18 + 18 + 20 + 14 = 111.
# But [11] says 96 lexical / 15 resolver!
# Let's see what [11] counted as 15 resolver features.
# In paper: "The 111 structured metrics span six cybersecurity feature families (20 + 21 + 18 + 18 + 20 + 14 = 111 raw; 20 + 8 + 18 + 18 + 20 + 14 = 98 retained)"
# Resolver features listed in paper:
# time_domain_activation, time_domain_expiration, ttl_hostname, asn_ip, time_response,
# qty_nameservers, qty_mx_servers, qty_ip_resolved, tls_ssl_certificate, domain_spf,
# qty_redirects, url_google_index, domain_google_index, url_shortened.
# Notice: url_shortened is 14. What could be the 15th feature in [11]?
# Let's list all 111 features to find which one [11] considered external/resolver vs lexical!
print("\n--- ALL RAW 111 FEATURES ---")
print(list(X_train_raw.columns))
