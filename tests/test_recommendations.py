import pytest
from app.recommendation_engine import (
    classify_risk,
    analyze_risk_drivers,
    retention_strategy,
    LOW_RISK_THRESHOLD,
    HIGH_RISK_THRESHOLD
)

def test_classify_risk_thresholds():
    """Ensure classification boundaries match standardized thresholds."""
    assert classify_risk(0.10) == "Low Risk"
    assert classify_risk(LOW_RISK_THRESHOLD - 0.01) == "Low Risk"
    assert classify_risk(LOW_RISK_THRESHOLD) == "Medium Risk"
    assert classify_risk(0.50) == "Medium Risk"
    assert classify_risk(HIGH_RISK_THRESHOLD - 0.01) == "Medium Risk"
    assert classify_risk(HIGH_RISK_THRESHOLD) == "High Risk"
    assert classify_risk(0.95) == "High Risk"

def test_analyze_risk_drivers():
    """Verify that churn drivers are identified accurately."""
    high_risk_cust = {
        "Contract": "Month-to-month",
        "tenure": 2,
        "InternetService": "Fiber optic",
        "TechSupport": "No",
        "OnlineSecurity": "No",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 95.0,
        "Partner": "No",
        "Dependents": "No"
    }
    drivers = analyze_risk_drivers(high_risk_cust)
    driver_factors = [d["factor"] for d in drivers]

    assert "Month-to-Month Contract" in driver_factors
    assert "New Customer (Tenure <= 6 mo)" in driver_factors
    assert "Fiber Optic without Support" in driver_factors
    assert "Electronic Check Billing" in driver_factors

def test_retention_strategy_output():
    """Verify that tailored retention strategies contain all required keys and playbooks."""
    cust = {
        "Contract": "Month-to-month",
        "tenure": 3,
        "PaymentMethod": "Electronic check",
        "TechSupport": "No"
    }
    plan = retention_strategy("High Risk", cust)

    assert "headline" in plan
    assert "primary_strategy" in plan
    assert "urgency" in plan
    assert "action_items" in plan
    assert "incentive_offer" in plan
    assert len(plan["action_items"]) > 0
