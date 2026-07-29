from app.database.database import SessionLocal
from app.database.models import (
    Customer,
    CollectionCase,
    Conversation,
    TimelineEvent,
)

from app.services.gemini_service import recommend_collection_strategy
from app.services.recommendation_service import save_recommendation


def recommend_strategy(customer_id: int):

    db = SessionLocal()

    # ------------------------------------
    # Get Customer
    # ------------------------------------
    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

    if not customer:
        db.close()
        return {"error": "Customer not found"}

    # ------------------------------------
    # Get Collection Case
    # ------------------------------------
    case = (
        db.query(CollectionCase)
        .filter(CollectionCase.customer_id == customer_id)
        .first()
    )

    # ------------------------------------
    # Get Conversation History
    # ------------------------------------
    conversations = (
        db.query(Conversation)
        .filter(Conversation.customer_id == customer_id)
        .order_by(Conversation.timestamp.asc())
        .all()
    )

    # ------------------------------------
    # Get Timeline Events
    # ------------------------------------
    timeline = (
        db.query(TimelineEvent)
        .filter(TimelineEvent.customer_id == customer_id)
        .order_by(TimelineEvent.created_at.desc())
        .all()
    )

    db.close()

    # ------------------------------------
    # Build AI Context
    # ------------------------------------
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
            "assigned_agent": case.assigned_agent if case else None,
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

    # ------------------------------------
    # Ask Gemini
    # ------------------------------------
    response = recommend_collection_strategy(context)

    # ------------------------------------
    # Save Recommendation
    # ------------------------------------
    save_recommendation(
        customer_id=customer.customer_id,
        recommendation=response,
    )

    # ------------------------------------
    # Return Recommendation
    # ------------------------------------
    return response