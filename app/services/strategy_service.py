from app.database.database import SessionLocal
from app.database.models import (
    Customer,
    CollectionCase,
    Conversation,
    TimelineEvent,
)

from app.services.gemini_service import recommend_collection_strategy
from app.services.recommendation_service import save_recommendation


# ==========================================================
# Normalize AI Confidence Score
# ==========================================================

def normalize_confidence(value) -> float:
    """
    Normalize Gemini confidence values to a 0.0 - 1.0 scale.

    Examples:
        0.95 -> 0.95
        90   -> 0.90
        95   -> 0.95
        100  -> 1.00
    """

    try:
        confidence = float(value)

        # Gemini may sometimes return percentage format
        if confidence > 1:
            confidence = confidence / 100

        # Keep confidence inside valid range
        confidence = max(0.0, min(confidence, 1.0))

        return round(confidence, 4)

    except (TypeError, ValueError):
        # Safe fallback if Gemini returns invalid data
        return 0.0


# ==========================================================
# AI Collection Strategy Recommendation
# ==========================================================

def recommend_strategy(customer_id: int):

    db = SessionLocal()

    try:

        # --------------------------------------------------
        # Get Customer
        # --------------------------------------------------
        customer = (
            db.query(Customer)
            .filter(Customer.customer_id == customer_id)
            .first()
        )

        if not customer:
            return {"error": "Customer not found"}

        # --------------------------------------------------
        # Get Collection Case
        # --------------------------------------------------
        case = (
            db.query(CollectionCase)
            .filter(CollectionCase.customer_id == customer_id)
            .first()
        )

        # --------------------------------------------------
        # Get Conversation History
        # --------------------------------------------------
        conversations = (
            db.query(Conversation)
            .filter(Conversation.customer_id == customer_id)
            .order_by(Conversation.timestamp.asc())
            .all()
        )

        # --------------------------------------------------
        # Get Timeline Events
        # --------------------------------------------------
        timeline = (
            db.query(TimelineEvent)
            .filter(TimelineEvent.customer_id == customer_id)
            .order_by(TimelineEvent.created_at.desc())
            .all()
        )

        # --------------------------------------------------
        # Build AI Context
        # --------------------------------------------------
        context = {
            "customer": {
                "customer_id": customer.customer_id,
                "name": customer.name,
                "loan_type": customer.loan_type,
                "loan_amount": customer.loan_amount,
                "emi": customer.emi,
                "outstanding": customer.outstanding,
                "days_overdue": customer.days_overdue,
            },

            "collection_case": {
                "status": case.status if case else None,
                "priority": case.priority if case else None,
                "assigned_agent": (
                    case.assigned_agent
                    if case
                    else None
                ),
                "next_followup": (
                    str(case.next_followup)
                    if case and case.next_followup
                    else None
                ),
            },

            "conversation_history": [
                {
                    "sender": c.sender,
                    "message": c.message,
                    "timestamp": str(c.timestamp),
                }
                for c in conversations
            ],

            "timeline": [
                {
                    "event_type": t.event_type,
                    "description": t.description,
                    "created_at": str(t.created_at),
                }
                for t in timeline
            ],
        }

        # --------------------------------------------------
        # Ask Gemini
        # --------------------------------------------------
        response = recommend_collection_strategy(context)

        # --------------------------------------------------
        # Normalize AI Response
        # --------------------------------------------------
        response["confidence"] = normalize_confidence(
            response.get("confidence")
        )

        # Normalize risk level for consistent database values
        if response.get("risk_level"):
            response["risk_level"] = (
                str(response["risk_level"])
                .strip()
                .upper()
            )

        # --------------------------------------------------
        # Save Recommendation
        # --------------------------------------------------
        save_recommendation(
            customer_id=customer.customer_id,
            recommendation=response,
        )

        # --------------------------------------------------
        # Return Recommendation
        # --------------------------------------------------
        return response

    finally:
        db.close()