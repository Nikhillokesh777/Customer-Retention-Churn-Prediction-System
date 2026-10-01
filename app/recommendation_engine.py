"""
Retention Recommendation Engine
Provides risk classification, driver analysis, and tailored retention playbooks.
"""
from typing import Dict, List, Any

# Standardized threshold constants across the entire system
LOW_RISK_THRESHOLD = 0.35
HIGH_RISK_THRESHOLD = 0.65


def classify_risk(probability: float) -> str:
    """Classifies churn probability into standardized risk tiers."""
    if probability < LOW_RISK_THRESHOLD:
        return "Low Risk"
    elif probability < HIGH_RISK_THRESHOLD:
        return "Medium Risk"
    else:
        return "High Risk"


def analyze_risk_drivers(customer: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Identifies specific churn risk factors present in a customer's profile.
    Returns a list of detected drivers with severity ratings and descriptions.
    """
    drivers = []

    # 1. Contract risk
    contract = customer.get("Contract", "")
    if contract == "Month-to-month":
        drivers.append({
            "factor": "Month-to-Month Contract",
            "severity": "High",
            "detail": "Customer has no long-term commitment and can cancel at any billing cycle."
        })

    # 2. Tenure risk (early life-cycle)
    tenure = float(customer.get("tenure", 0))
    if tenure <= 6:
        drivers.append({
            "factor": "New Customer (Tenure <= 6 mo)",
            "severity": "High",
            "detail": "High risk of early churn during the critical onboarding window."
        })
    elif tenure <= 18:
        drivers.append({
            "factor": "Moderate Tenure (7-18 mo)",
            "severity": "Medium",
            "detail": "Customer is approaching renewal evaluation phase."
        })

    # 3. Fiber Optic without Support / Security
    internet = customer.get("InternetService", "")
    tech_sup = customer.get("TechSupport", "")
    online_sec = customer.get("OnlineSecurity", "")
    if internet == "Fiber optic" and (tech_sup == "No" or online_sec == "No"):
        drivers.append({
            "factor": "Fiber Optic without Support",
            "severity": "High",
            "detail": "High-speed tier customer lacks technical support or online security protection."
        })

    # 4. Payment friction
    payment = customer.get("PaymentMethod", "")
    if payment == "Electronic check":
        drivers.append({
            "factor": "Electronic Check Billing",
            "severity": "Medium",
            "detail": "Manual electronic checks correlate with higher churn than automated billing."
        })

    # 5. Price sensitivity
    monthly = float(customer.get("MonthlyCharges", 0))
    if monthly > 80.0 and contract == "Month-to-month":
        drivers.append({
            "factor": "High Monthly Spend on Flexible Plan",
            "severity": "High",
            "detail": f"Paying ${monthly:.2f}/mo without contract discounts; susceptible to competitor pricing."
        })

    # 6. Low household stickiness
    partner = customer.get("Partner", "")
    dependents = customer.get("Dependents", "")
    if partner == "No" and dependents == "No":
        drivers.append({
            "factor": "Single Account Footprint",
            "severity": "Low",
            "detail": "Single user account with fewer tied family members, lower switching barrier."
        })

    return drivers


def retention_strategy(risk: str, customer: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generates an actionable, personalized retention playbook based on risk tier
    and specific customer account attributes.
    """
    if customer is None:
        customer = {}

    drivers = analyze_risk_drivers(customer)

    if risk == "High Risk":
        action_items = []
        incentives = []

        if customer.get("Contract") == "Month-to-month":
            action_items.append("Offer a 15% discount in exchange for signing an annual (1-year) contract.")
            incentives.append("Annual Contract 15% Discount")

        if customer.get("PaymentMethod") == "Electronic check":
            action_items.append("Provide a $10 one-time bill credit to enroll in Auto-Pay (Bank transfer / Credit card).")
            incentives.append("$10 Auto-Pay Credit")

        if customer.get("TechSupport") == "No" or customer.get("OnlineSecurity") == "No":
            action_items.append("Grant 3 months complimentary Premium Tech Support & Online Security.")
            incentives.append("3-Month Free Tech Support & Security Bundle")

        if not action_items:
            action_items.append("Schedule a dedicated customer success outreach call within 24 hours.")
            action_items.append("Offer a personalized service review and loyalty billing concession.")
            incentives.append("10% Loyalty Concession")

        return {
            "headline": "🚨 Immediate Retention Intervention Required",
            "primary_strategy": "Contract Commitment & Value Re-alignment",
            "urgency": "Immediate (within 24–48 hours)",
            "action_items": action_items,
            "incentive_offer": " + ".join(incentives) if incentives else "Targeted Account Discount",
            "drivers": drivers
        }

    elif risk == "Medium Risk":
        action_items = []
        incentives = []

        if float(customer.get("tenure", 0)) <= 12:
            action_items.append("Send proactive check-in survey to evaluate satisfaction and service usage.")
            incentives.append("Complimentary Speed or Feature Boost for 30 Days")

        if customer.get("PaymentMethod") == "Electronic check":
            action_items.append("Promote paperless & automated billing with a small recurring monthly savings.")
            incentives.append("$5/mo Auto-Pay Savings")

        if not action_items:
            action_items.append("Trigger engagement email showcasing unused benefits and bundle options.")
            incentives.append("Service Upgrade Trial")

        return {
            "headline": "⚠️ Proactive Account Stabilization",
            "primary_strategy": "Engagement & Loyalty Building",
            "urgency": "Within 7 business days",
            "action_items": action_items,
            "incentive_offer": " + ".join(incentives) if incentives else "Engagement Loyalty Perk",
            "drivers": drivers
        }

    else:  # Low Risk
        return {
            "headline": "✅ Relationship Maintenance & Upsell Opportunity",
            "primary_strategy": "Maintain Delight & Explore Account Expansion",
            "urgency": "Quarterly Routine Review",
            "action_items": [
                "Maintain service excellence and ensure billing stability.",
                "Send annual appreciation reward or loyalty milestone recognition.",
                "Assess eligibility for premium add-ons or multi-device family plans."
            ],
            "incentive_offer": "Loyalty Milestone Perks",
            "drivers": drivers
        }