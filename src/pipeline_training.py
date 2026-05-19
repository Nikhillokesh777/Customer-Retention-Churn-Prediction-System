import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

from sklearn.impute import SimpleImputer

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, classification_report

import joblib
import os

# =========================================
# Load Dataset
# =========================================

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "WA_Fn-UseC_-Telco-Customer-Churn.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "churn_pipeline.pkl")

df = pd.read_csv(DATA_PATH)

# =========================================
# Basic Cleaning
# =========================================

df.drop("customerID", axis=1, inplace=True)

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

# =========================================
# Encode Target
# =========================================

df["Churn"] = df["Churn"].map({
    "Yes": 1,
    "No": 0
})

# =========================================
# Features and Target
# =========================================

X = df.drop("Churn", axis=1)

y = df["Churn"]

# =========================================
# Numerical & Categorical Columns
# =========================================

numerical_cols = [
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]

categorical_cols = [
    col for col in X.columns
    if col not in numerical_cols
]

# =========================================
# Numerical Pipeline
# =========================================

numerical_transformer = Pipeline(steps=[

    (
        "imputer",
        SimpleImputer(strategy="median")
    ),

    (
        "scaler",
        StandardScaler()
    )
])

# =========================================
# Categorical Pipeline
# =========================================

categorical_transformer = Pipeline(steps=[

    (
        "imputer",
        SimpleImputer(strategy="most_frequent")
    ),

    (
        "onehot",
        OneHotEncoder(handle_unknown="ignore")
    )
])

# =========================================
# Combine Preprocessing
# =========================================

preprocessor = ColumnTransformer(

    transformers=[

        (
            "num",
            numerical_transformer,
            numerical_cols
        ),

        (
            "cat",
            categorical_transformer,
            categorical_cols
        )
    ]
)

# =========================================
# Full Pipeline
# =========================================

model_pipeline = Pipeline(steps=[

    (
        "preprocessor",
        preprocessor
    ),

    (
        "model",
        RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
    )
])

# =========================================
# Train-Test Split
# =========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42,

    stratify=y
)

# =========================================
# Train Pipeline
# =========================================

if __name__ == "__main__":
    model_pipeline.fit(X_train, y_train)

# =========================================
# Predictions
# =========================================

y_pred = model_pipeline.predict(X_test)

# =========================================
# Accuracy
# =========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print(f"Accuracy : {accuracy:.4f}")
print(classification_report(y_test, y_pred))

# =========================================
# Save Pipeline
# =========================================

joblib.dump(model_pipeline, MODEL_PATH)
print(f"Pipeline saved to {MODEL_PATH}")