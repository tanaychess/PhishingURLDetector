"""
Experiment script: Run feature reduction and dimensional benchmarking across SHAP-ranked subsets.
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_config, load_dataset, split_and_save_data
from src.preprocessing import PhishingPreprocessor
from src.feature_selection import run_feature_selection_experiments

def run(X_train_df=None, y_train=None, X_test_df=None, y_test=None, global_importance_df=None):
    config = load_config()
    
    if X_train_df is None or global_importance_df is None:
        df = load_dataset(config["dataset"]["raw_path"], config["dataset"]["target_column"])
        X_train, X_test, y_train, y_test = split_and_save_data(df, config)
        preprocessor = PhishingPreprocessor(remove_constant=True, scale_features=False)
        X_train_df = preprocessor.fit_transform(X_train, return_df=True)
        X_test_df = preprocessor.transform(X_test, return_df=True)
        
        shap_csv = os.path.join(config["paths"]["results_explanations"], "shap_global_feature_importance.csv")
        assert os.path.exists(shap_csv), f"Run explainability experiment first to generate {shap_csv}"
        global_importance_df = pd.read_csv(shap_csv)
        
    fs_df = run_feature_selection_experiments(
        X_train_df, y_train, X_test_df, y_test, global_importance_df, config
    )
    return fs_df

if __name__ == "__main__":
    run()
