"""
Model architecture factory: instantiates machine learning models with configuration parameters.
Uses standard scaling pipelines for linear models to ensure fast, stable convergence and zero data leakage.
"""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import xgboost as xgb

def get_models(config):
    """
    Instantiate and return a dictionary of baseline and state-of-the-art ML models.
    """
    seed = config["project"]["random_seed"]
    cfg_models = config["models"]
    
    # 1. Logistic Regression (L2 regularized with Standard Scaling Pipeline)
    lr_cfg = cfg_models["logistic_regression"]
    lr_model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(
            max_iter=lr_cfg.get("max_iter", 1000),
            C=lr_cfg.get("C", 1.0),
            solver="lbfgs",
            random_state=seed
        ))
    ])
    
    # 2. Decision Tree (Depth-bounded white-box)
    dt_cfg = cfg_models["decision_tree"]
    dt_model = DecisionTreeClassifier(
        max_depth=dt_cfg.get("max_depth", 12),
        min_samples_split=dt_cfg.get("min_samples_split", 10),
        min_samples_leaf=dt_cfg.get("min_samples_leaf", 5),
        random_state=seed
    )
    
    # 3. Random Forest (Ensemble bagging)
    rf_cfg = cfg_models["random_forest"]
    rf_model = RandomForestClassifier(
        n_estimators=rf_cfg.get("n_estimators", 100),
        max_depth=rf_cfg.get("max_depth", 15),
        min_samples_split=rf_cfg.get("min_samples_split", 5),
        min_samples_leaf=rf_cfg.get("min_samples_leaf", 2),
        n_jobs=-1,
        random_state=seed
    )
    
    # 4. Linear Support Vector Machine (Scaled with Platt calibration)
    svm_cfg = cfg_models["linear_svm"]
    base_svc = LinearSVC(
        C=svm_cfg.get("C", 1.0),
        max_iter=svm_cfg.get("max_iter", 2000),
        random_state=seed,
        dual="auto"
    )
    svm_model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", CalibratedClassifierCV(estimator=base_svc, cv=3))
    ])
    
    # 5. XGBoost (Gradient-boosted decision trees)
    xgb_cfg = config["models"]["xgboost"]
    xgb_model = xgb.XGBClassifier(
        n_estimators=xgb_cfg.get("n_estimators", 100),
        max_depth=xgb_cfg.get("max_depth", 6),
        learning_rate=xgb_cfg.get("learning_rate", 0.1),
        subsample=xgb_cfg.get("subsample", 0.8),
        colsample_bytree=xgb_cfg.get("colsample_bytree", 0.8),
        eval_metric=xgb_cfg.get("eval_metric", "logloss"),
        random_state=seed,
        n_jobs=-1,
        tree_method="hist"
    )
    
    models = {
        "Logistic Regression": lr_model,
        "Decision Tree": dt_model,
        "Random Forest": rf_model,
        "Linear SVM": svm_model,
        "XGBoost": xgb_model
    }
    
    return models
