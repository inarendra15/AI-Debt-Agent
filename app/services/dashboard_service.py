from sqlalchemy import func

from app.database.database import SessionLocal
from app.database.models import Customer


def get_dashboard():
    db = SessionLocal()

    total_customers = db.query(Customer).count()

    total_outstanding = (
        db.query(func.sum(Customer.outstanding))
        .scalar()
    ) or 0

    average_outstanding = (
        db.query(func.avg(Customer.outstanding))
        .scalar()
    ) or 0

    high_risk_cases = (
        db.query(Customer)
        .filter(Customer.days_overdue >= 90)
        .count()
    )

    active_cases = (
        db.query(Customer)
        .filter(Customer.outstanding > 0)
        .count()
    )

    db.close()

    return {
        "total_customers": total_customers,
        "active_cases": active_cases,
        "high_risk_cases": high_risk_cases,
        "total_outstanding": round(total_outstanding, 2),
        "average_outstanding": round(average_outstanding, 2),
    }