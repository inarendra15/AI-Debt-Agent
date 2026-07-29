from sqlalchemy import func

from app.database.database import SessionLocal
from app.database.models import Customer


def get_dashboard_analytics():

    db = SessionLocal()

    total_customers = db.query(Customer).count()

    total_outstanding = (
        db.query(
            func.sum(Customer.outstanding)
        ).scalar()
        or 0
    )

    average_outstanding = (
        db.query(
            func.avg(Customer.outstanding)
        ).scalar()
        or 0
    )

    average_overdue = (
        db.query(
            func.avg(Customer.days_overdue)
        ).scalar()
        or 0
    )

    high_overdue = (
        db.query(Customer)
        .filter(Customer.days_overdue >= 60)
        .count()
    )

    loan_distribution = (
        db.query(
            Customer.loan_type,
            func.count(Customer.customer_id)
        )
        .group_by(Customer.loan_type)
        .all()
    )

    db.close()

    return {
        "total_customers": total_customers,
        "total_outstanding": total_outstanding,
        "average_outstanding": round(average_outstanding, 2),
        "average_overdue_days": round(average_overdue, 2),
        "high_overdue_customers": high_overdue,
        "loan_distribution": {
            loan: count
            for loan, count in loan_distribution
        }
    }