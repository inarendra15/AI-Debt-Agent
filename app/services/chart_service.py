from sqlalchemy import func

from app.database.database import SessionLocal
from app.database.models import Customer


def get_chart_data():

    db = SessionLocal()

    loan_data = (
        db.query(
            Customer.loan_type,
            func.count(Customer.customer_id)
        )
        .group_by(Customer.loan_type)
        .all()
    )

    bucket_0_30 = (
        db.query(Customer)
        .filter(Customer.days_overdue <= 30)
        .count()
    )

    bucket_31_60 = (
        db.query(Customer)
        .filter(Customer.days_overdue.between(31, 60))
        .count()
    )

    bucket_61_90 = (
        db.query(Customer)
        .filter(Customer.days_overdue.between(61, 90))
        .count()
    )

    bucket_90 = (
        db.query(Customer)
        .filter(Customer.days_overdue > 90)
        .count()
    )

    db.close()

    return {
        "loan_distribution": {
            loan: count
            for loan, count in loan_data
        },
        "overdue_distribution": {
            "0-30": bucket_0_30,
            "31-60": bucket_31_60,
            "61-90": bucket_61_90,
            "90+": bucket_90
        }
    }