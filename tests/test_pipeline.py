import os
import pytest
import pandas as pd
import numpy as np
from app.utils import load_pipeline

@pytest.fixture(scope="module")
def pipeline():
    return load_pipeline()

def test_pipeline_loading(pipeline):
    """Ensure trained pipeline loads correctly."""
    assert pipeline is not None
    assert hasattr(pipeline, "predict")
    assert hasattr(pipeline, "predict_proba")

def test_pipeline_prediction_shape_and_bounds(pipeline):
    """Validate prediction outputs and probability bounds."""
    sample = pd.DataFrame([{
        "tenure": 12,
        "MonthlyCharges": 70.0,
        "TotalCharges": 840.0,
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "No",
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check"
    }])

    pred = pipeline.predict(sample)
    proba = pipeline.predict_proba(sample)

    assert len(pred) == 1
    assert pred[0] in [0, 1]
    assert proba.shape == (1, 2)
    assert 0.0 <= proba[0][1] <= 1.0
    assert np.isclose(proba[0][0] + proba[0][1], 1.0)

def test_senior_citizen_encoding(pipeline):
    """Verify that integer SeniorCitizen (0 and 1) is accepted without warnings/errors."""
    row_0 = {
        "tenure": 5, "MonthlyCharges": 50.0, "TotalCharges": 250.0,
        "gender": "Male", "SeniorCitizen": 0, "Partner": "No",
        "Dependents": "No", "PhoneService": "Yes", "MultipleLines": "No",
        "InternetService": "DSL", "OnlineSecurity": "Yes", "OnlineBackup": "No",
        "DeviceProtection": "No", "TechSupport": "Yes", "StreamingTV": "No",
        "StreamingMovies": "No", "Contract": "Month-to-month", "PaperlessBilling": "No",
        "PaymentMethod": "Mailed check"
    }
    row_1 = dict(row_0)
    row_1["SeniorCitizen"] = 1

    df_0 = pd.DataFrame([row_0])
    df_1 = pd.DataFrame([row_1])

    prob_0 = pipeline.predict_proba(df_0)[0][1]
    prob_1 = pipeline.predict_proba(df_1)[0][1]

    assert 0.0 <= prob_0 <= 1.0
    assert 0.0 <= prob_1 <= 1.0
