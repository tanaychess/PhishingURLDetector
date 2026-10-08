"""
Experiment script: Train and evaluate baseline and ensemble ML models on static URL features.
"""

import os
import sys

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_config, load_dataset, split_and_save_data
from src.preprocessing import PhishingPreprocessor
from src.train import train_and_evaluate_all
from src.generate_paper_figures import (
    plot_system_architecture,
    plot_class_distribution,
    plot_model_comparison,
    plot_confusion_matrices,
    plot_roc_pr_curves
)

def run():
    config = load_config()
    print("Loading dataset...")
    df = load_dataset(config["dataset"]["raw_path"], config["dataset"]["target_column"])
    
    X_train, X_test, y_train, y_test = split_and_save_data(df, config)
    
    preprocessor = PhishingPreprocessor(remove_constant=True, scale_features=False)
    X_train_df = preprocessor.fit_transform(X_train, return_df=True)
    X_test_df = preprocessor.transform(X_test, return_df=True)
    
    results_df, trained_models, test_predictions, test_probabilities = train_and_evaluate_all(
        X_train_df, y_train, X_test_df, y_test, config, preprocessor.feature_names
    )
    
    fig_dir = config["paths"]["figures"]
    plot_system_architecture(fig_dir)
    plot_class_distribution(y_train, y_test, fig_dir)
    plot_model_comparison(results_df, fig_dir)
    plot_confusion_matrices(y_test, test_predictions, fig_dir)
    plot_roc_pr_curves(y_test, test_probabilities, fig_dir)
    
    return results_df, trained_models, X_train_df, X_test_df, y_train, y_test, preprocessor.feature_names

if __name__ == "__main__":
    run()
