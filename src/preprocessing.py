"""
Preprocessing module: handles feature normalization, scaling, and variance filtering.
Guarantees zero data leakage by fitting transformers strictly on training partition.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold

class PhishingPreprocessor:
    def __init__(self, remove_constant=True, scale_features=True):
        self.remove_constant = remove_constant
        self.scale_features = scale_features
        self.variance_selector = None
        self.scaler = None
        self.feature_names = None
        
    def fit(self, X_train: pd.DataFrame):
        """Fit variance selector and scaler strictly on training DataFrame."""
        current_X = X_train.copy()
        
        if self.remove_constant:
            self.variance_selector = VarianceThreshold(threshold=0.0)
            self.variance_selector.fit(current_X)
            retained_cols = current_X.columns[self.variance_selector.get_support()]
            current_X = current_X[retained_cols]
        else:
            retained_cols = current_X.columns
            
        self.feature_names = list(retained_cols)
        
        if self.scale_features:
            self.scaler = StandardScaler()
            self.scaler.fit(current_X)
            
        return self
        
    def transform(self, X: pd.DataFrame, return_df: bool = False):
        """Transform given DataFrame using fitted transformers."""
        if self.variance_selector is not None:
            X_filtered = X[self.feature_names].copy()
        else:
            X_filtered = X.copy()
            
        if self.scaler is not None:
            X_scaled = self.scaler.transform(X_filtered)
        else:
            X_scaled = X_filtered.values
            
        if return_df:
            return pd.DataFrame(X_scaled, columns=self.feature_names, index=X.index)
        return X_scaled

    def fit_transform(self, X_train: pd.DataFrame, return_df: bool = False):
        return self.fit(X_train).transform(X_train, return_df=return_df)
