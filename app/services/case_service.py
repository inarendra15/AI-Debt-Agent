from app.database.database import SessionLocal
from app.database.models import CollectionCase


def create_case(data):

    db = SessionLocal()

    case = CollectionCase(
        customer_id=data.customer_id,
        assigned_agent=data.assigned_agent,
        priority=data.priority
    )

    db.add(case)
    db.commit()
    db.refresh(case)

    db.close()

    return case


def get_all_cases():

    db = SessionLocal()

    cases = db.query(CollectionCase).all()

    db.close()

    return cases


def get_case(case_id):

    db = SessionLocal()

    case = (
        db.query(CollectionCase)
        .filter(CollectionCase.id == case_id)
        .first()
    )

    db.close()

    return case


def update_case(case_id, data):

    db = SessionLocal()

    case = (
        db.query(CollectionCase)
        .filter(CollectionCase.id == case_id)
        .first()
    )

    if not case:
        db.close()
        return None

    if data.status is not None:
        case.status = data.status

    if data.assigned_agent is not None:
        case.assigned_agent = data.assigned_agent

    if data.priority is not None:
        case.priority = data.priority

    if data.next_followup is not None:
        case.next_followup = data.next_followup

    db.commit()
    db.refresh(case)

    db.close()

    return case