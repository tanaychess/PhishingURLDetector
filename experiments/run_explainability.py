"""
Experiment script: Run TreeSHAP explainability on trained models and produce global/local explanations.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_config, load_dataset, split_and_save_data
from src.preprocessing import PhishingPreprocessor
from src.models import get_models
from src.explainability import run_shap_analysis

def run(model=None, X_train_df=None, X_test_df=None, y_train=None, y_test=None, feature_names=None):
    config = load_config()
    
    if model is None:
        df = load_dataset(config["dataset"]["raw_path"], config["dataset"]["target_column"])
        X_train, X_test, y_train, y_test = split_and_save_data(df, config)
        preprocessor = PhishingPreprocessor(remove_constant=True, scale_features=False)
        X_train_df = preprocessor.fit_transform(X_train, return_df=True)
        X_test_df = preprocessor.transform(X_test, return_df=True)
        feature_names = preprocessor.feature_names
        
        models = get_models(config)
        model = models["XGBoost"]
        print("Training XGBoost for SHAP analysis...")
        model.fit(X_train_df, y_train)
        
    global_importance_df, local_df = run_shap_analysis(
        model, X_train_df, X_test_df, y_test, config, feature_names
    )
    
    return global_importance_df, local_df

if __name__ == "__main__":
    run()
