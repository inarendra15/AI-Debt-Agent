from app.database.database import SessionLocal
from app.database.models import CollectionCase
from app.services.timeline_service import log_event


# ======================================================
# Create Collection Case
# ======================================================

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

    # Timeline Entry
    log_event(
        customer_id=case.customer_id,
        case_id=case.id,
        event_type="case_created",
        description=f"Collection case #{case.id} created and assigned to {case.assigned_agent}."
    )

    db.close()

    return case


# ======================================================
# Get All Cases
# ======================================================

def get_all_cases():

    db = SessionLocal()

    cases = db.query(CollectionCase).all()

    db.close()

    return cases


# ======================================================
# Get Single Case
# ======================================================

def get_case(case_id):

    db = SessionLocal()

    case = (
        db.query(CollectionCase)
        .filter(CollectionCase.id == case_id)
        .first()
    )

    db.close()

    return case


# ======================================================
# Update Collection Case
# ======================================================

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

    changes = []

    # Assigned Agent
    if (
        data.assigned_agent is not None
        and data.assigned_agent != case.assigned_agent
    ):
        changes.append(
            f"Assigned Agent: {case.assigned_agent} → {data.assigned_agent}"
        )
        case.assigned_agent = data.assigned_agent

    # Status
    if (
        data.status is not None
        and data.status != case.status
    ):
        changes.append(
            f"Status: {case.status} → {data.status}"
        )
        case.status = data.status

    # Priority
    if (
        data.priority is not None
        and data.priority != case.priority
    ):
        changes.append(
            f"Priority: {case.priority} → {data.priority}"
        )
        case.priority = data.priority

    # Follow-up Date
    if (
        data.next_followup is not None
        and data.next_followup != case.next_followup
    ):
        changes.append(
            f"Next Follow-up updated to {data.next_followup}"
        )
        case.next_followup = data.next_followup

    db.commit()
    db.refresh(case)

    # Timeline Entry
    if changes:
        log_event(
            customer_id=case.customer_id,
            case_id=case.id,
            event_type="case_updated",
            description=" | ".join(changes)
        )

    db.close()

    return case