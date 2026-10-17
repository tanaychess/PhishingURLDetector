"""
Data loader and dataset integrity validator.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import yaml

def load_config(config_path="config/config.yaml"):
    """Load configuration dictionary from YAML file."""
    if not os.path.exists(config_path):
        # Check parent directory fallback
        alt_path = os.path.join(os.path.dirname(__file__), "..", config_path)
        if os.path.exists(alt_path):
            config_path = alt_path
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def load_dataset(raw_path="data/raw/dataset_small.csv", target_col="phishing"):
    """
    Load raw phishing dataset and perform basic integrity verification.
    """
    if not os.path.exists(raw_path):
        alt_path = os.path.join(os.path.dirname(__file__), "..", raw_path)
        if os.path.exists(alt_path):
            raw_path = alt_path
        else:
            raise FileNotFoundError(f"Raw dataset not found at {raw_path}")

    df = pd.read_csv(raw_path)
    
    # Validation checks
    assert target_col in df.columns, f"Target column '{target_col}' missing from dataset!"
    assert df.shape[0] > 0, "Dataset is empty!"
    
    # Handle any nulls if present (dataset is clean, but defensive check)
    if df.isnull().sum().sum() > 0:
        df = df.fillna(df.median(numeric_only=True))
        
    return df

def split_and_save_data(df, config):
    """
    Split dataset into Stratified Train and Test sets and save to processed directory.
    """
    target_col = config["dataset"]["target_column"]
    test_size = config["dataset"]["test_size"]
    random_seed = config["project"]["random_seed"]
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_seed,
        stratify=y if config["dataset"]["stratify"] else None
    )
    
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    
    train_path = config["dataset"]["processed_train_path"]
    test_path = config["dataset"]["processed_test_path"]
    
    os.makedirs(os.path.dirname(train_path), exist_ok=True)
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print(f"Data split successfully:")
    print(f"  Training set: {train_df.shape[0]} samples ({train_df.shape[1]-1} features)")
    print(f"  Testing set:  {test_df.shape[0]} samples ({test_df.shape[1]-1} features)")
    print(f"  Class balance (Train): {dict(y_train.value_counts())}")
    print(f"  Class balance (Test):  {dict(y_test.value_counts())}")
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    cfg = load_config()
    data = load_dataset(cfg["dataset"]["raw_path"], cfg["dataset"]["target_column"])
    split_and_save_data(data, cfg)
