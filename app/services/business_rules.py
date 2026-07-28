def evaluate_case(ai_result: dict) -> dict:
    """
    Evaluate AI output and determine backend workflow actions.
    """

    workflow = {
        "status": "pending",
        "action": "none",
        "priority": "normal",
        "escalate": False,
    }

    intent = ai_result.get("intent")
    risk = ai_result.get("risk_level")
    human = ai_result.get("need_human_agent")
    followup = ai_result.get("followup_days")

    # Promise to pay
    if intent == "promise_to_pay":
        workflow["status"] = "payment_promised"
        workflow["action"] = "schedule_followup"

        if followup:
            workflow["followup_days"] = followup

    # Financial hardship
    elif intent == "financial_hardship":
        workflow["status"] = "hardship_case"
        workflow["action"] = "offer_repayment_plan"

    # Payment claim
    elif intent == "payment_claim":
        workflow["status"] = "payment_under_verification"
        workflow["action"] = "verify_payment"

    # Complaint
    elif intent == "complaint":
        workflow["status"] = "customer_complaint"
        workflow["action"] = "human_review"
        workflow["escalate"] = True

    # Unable to pay
    elif intent == "unable_to_pay":
        workflow["status"] = "payment_difficulty"
        workflow["action"] = "review_case"

    # High-risk accounts
    if risk == "high":
        workflow["priority"] = "high"

    # Human escalation
    if human:
        workflow["escalate"] = True

    return workflow