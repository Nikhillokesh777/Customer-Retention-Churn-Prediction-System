"""
End-to-end model pipeline training and evaluation.
Builds preprocessing and classification pipeline for customer churn prediction.
"""
import os
import argparse
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "WA_Fn-UseC_-Telco-Customer-Churn.csv")
DEFAULT_MODEL_PATH = os.path.join(BASE_DIR, "models", "churn_pipeline.pkl")


def load_and_clean_data(data_path: str = DEFAULT_DATA_PATH):
    """Loads and performs initial cleaning on the Telco Customer Churn dataset."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")

    df = pd.read_csv(data_path)

    # Drop non-predictive identifier
    if "customerID" in df.columns:
        df = df.drop(columns=["customerID"])

    # TotalCharges contains blank strings for 0-tenure customers
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # Map target
    if "Churn" in df.columns:
        df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    return df


def build_pipeline(model_type: str = "xgboost"):
    """Constructs the full ColumnTransformer and Classifier pipeline."""
    numerical_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    categorical_cols = [
        "gender", "SeniorCitizen", "Partner", "Dependents",
        "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies",
        "Contract", "PaperlessBilling", "PaymentMethod"
    ]

    numerical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numerical_transformer, numerical_cols),
        ("cat", categorical_transformer, categorical_cols)
    ])

    if model_type == "xgboost":
        # Balanced XGBoost with scale_pos_weight for high churn recall
        classifier = XGBClassifier(
            n_estimators=120,
            max_depth=3,
            learning_rate=0.08,
            scale_pos_weight=2.0,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric="logloss"
        )
    elif model_type == "random_forest":
        classifier = RandomForestClassifier(
            n_estimators=100,
            class_weight="balanced",
            random_state=42
        )
    else:
        raise ValueError(f"Unknown model_type: {model_type}")

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", classifier)
    ])

    return pipeline


def train_and_evaluate(
    data_path: str = DEFAULT_DATA_PATH,
    model_output_path: str = DEFAULT_MODEL_PATH,
    model_type: str = "xgboost",
    test_size: float = 0.2,
    random_state: int = 42
):
    """Executes the full training, evaluation, and serialization workflow."""
    print(f"Loading data from {data_path}...")
    df = load_and_clean_data(data_path)

    X = df.drop(columns=["Churn"])
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    print(f"Building pipeline (model_type='{model_type}')...")
    pipeline = build_pipeline(model_type=model_type)

    print("Fitting model...")
    pipeline.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)

    print("\n" + "=" * 45)
    print("           MODEL EVALUATION SUMMARY          ")
    print("=" * 45)
    print(f"Accuracy  : {acc:.4f}")
    print(f"Precision : {prec:.4f}")
    print(f"Recall    : {rec:.4f}  (Churn capture rate)")
    print(f"F1-Score  : {f1:.4f}")
    print(f"ROC-AUC   : {auc:.4f}")
    print("=" * 45 + "\n")
    print(classification_report(y_test, y_pred, target_names=["Retain (0)", "Churn (1)"]))

    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(pipeline, model_output_path)
    print(f"Successfully saved trained pipeline to: {model_output_path}")

    return pipeline, {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "auc": auc
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Churn Prediction Pipeline")
    parser.add_argument("--data", default=DEFAULT_DATA_PATH, help="Path to raw CSV dataset")
    parser.add_argument("--out", default=DEFAULT_MODEL_PATH, help="Path to save trained pipeline")
    parser.add_argument("--model", choices=["xgboost", "random_forest"], default="xgboost", help="Classifier type")
    args = parser.parse_args()

    train_and_evaluate(
        data_path=args.data,
        model_output_path=args.out,
        model_type=args.model
    )