def generate_analytics(ai_response):
    """
    Generate internal analytics from AI response.
    """

    intent = ai_response.get("intent", "")
    sentiment = ai_response.get("sentiment", "")
    risk = ai_response.get("risk_level", "")

    analytics = {
        "risk_score": 50,
        "probability_of_payment": 50,
        "customer_cooperation": "Medium",
        "financial_stress": "Medium",
        "recommended_plan": "Continue follow-up",
        "escalation_reason": None
    }

    if intent == "promise_to_pay":
        analytics["probability_of_payment"] = 85
        analytics["customer_cooperation"] = "High"
        analytics["recommended_plan"] = "Schedule follow-up"

    elif intent == "cannot_pay":
        analytics["probability_of_payment"] = 30
        analytics["financial_stress"] = "High"
        analytics["recommended_plan"] = "Offer restructuring"

    elif intent == "refusal":
        analytics["probability_of_payment"] = 10
        analytics["customer_cooperation"] = "Low"
        analytics["recommended_plan"] = "Escalate"

    if risk == "high":
        analytics["risk_score"] = 85

    elif risk == "medium":
        analytics["risk_score"] = 60

    else:
        analytics["risk_score"] = 35

    if sentiment == "negative":
        analytics["financial_stress"] = "High"

    if analytics["risk_score"] >= 80:
        analytics["escalation_reason"] = "High risk customer"

    return analytics