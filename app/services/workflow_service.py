from datetime import datetime, timedelta

from app.database.database import SessionLocal
from app.database.models import CollectionCase


def apply_ai_workflow(customer_id: int, ai_result: dict):

    db = SessionLocal()

    case = (
        db.query(CollectionCase)
        .filter(CollectionCase.customer_id == customer_id)
        .first()
    )

    if not case:
        db.close()
        return None

    intent = ai_result.get("intent", "").lower()
    sentiment = ai_result.get("sentiment", "").lower()
    risk = ai_result.get("risk_level", "").lower()
    followup_days = ai_result.get("followup_days")

    # Status mapping
    if "promise" in intent:
        case.status = "PROMISE_TO_PAY"

    elif "paid" in intent:
        case.status = "CLOSED"

    elif "callback" in intent:
        case.status = "FOLLOW_UP"

    elif "refuse" in intent:
        case.status = "ESCALATED"

    else:
        case.status = "CONTACTED"

    # Priority mapping
    if risk == "high":
        case.priority = "HIGH"
    elif risk == "medium":
        case.priority = "MEDIUM"
    else:
        case.priority = "LOW"

    # Escalate angry customers
    if sentiment == "negative":
        case.priority = "HIGH"

    # Schedule next follow-up
    if followup_days:
        case.next_followup = (
            datetime.utcnow() +
            timedelta(days=int(followup_days))
        )

    db.commit()
    db.refresh(case)

    db.close()

    return case