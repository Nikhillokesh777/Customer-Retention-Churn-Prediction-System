def classify_risk(probability):

    if probability < 0.3:
        return "Low Risk"

    elif probability < 0.7:
        return "Medium Risk"

    else:
        return "High Risk"


def retention_strategy(risk):

    if risk == "High Risk":
        return "Offer discount and premium support"

    elif risk == "Medium Risk":
        return "Send engagement offers"

    else:
        return "Maintain customer satisfaction"