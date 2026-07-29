from app.database.database import SessionLocal
from app.database.models import Conversation


def add_message(customer_id: int, sender: str, message: str):
    db = SessionLocal()

    conversation = Conversation(
        customer_id=customer_id,
        sender=sender,
        message=message
    )

    db.add(conversation)
    db.commit()
    db.close()


def get_history(customer_id: int):
    db = SessionLocal()

    conversations = (
        db.query(Conversation)
        .filter(Conversation.customer_id == customer_id)
        .order_by(Conversation.timestamp.asc())
        .all()
    )

    db.close()

    return [
        {
            "role": conv.sender,
            "message": conv.message
        }
        for conv in conversations
    ]