from app.database.database import SessionLocal
from app.database.models import TimelineEvent


def log_event(
    customer_id: int,
    event_type: str,
    description: str,
    case_id: int = None,
):
    """
    Store an event in the customer timeline.
    """

    db = SessionLocal()

    event = TimelineEvent(
        customer_id=customer_id,
        case_id=case_id,
        event_type=event_type,
        description=description,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    db.close()

    return event

from app.database.models import TimelineEvent


def get_customer_timeline(customer_id: int):

    db = SessionLocal()

    events = (
        db.query(TimelineEvent)
        .filter(TimelineEvent.customer_id == customer_id)
        .order_by(TimelineEvent.created_at.desc())
        .all()
    )

    db.close()

    return events