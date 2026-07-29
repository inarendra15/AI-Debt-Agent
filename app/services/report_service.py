from app.database.database import SessionLocal
from app.database.models import Customer


def get_reports():

    db = SessionLocal()

    # Top defaulters
    top_defaulters = (
        db.query(Customer)
        .order_by(Customer.outstanding.desc())
        .limit(5)
        .all()
    )

    # Highest EMI customers
    highest_emi = (
        db.query(Customer)
        .order_by(Customer.emi.desc())
        .limit(5)
        .all()
    )

    # Overdue buckets
    bucket_0_30 = db.query(Customer).filter(Customer.days_overdue <= 30).count()

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
        "top_defaulters": [
            {
                "customer_id": c.customer_id,
                "name": c.name,
                "outstanding": c.outstanding
            }
            for c in top_defaulters
        ],
        "highest_emi_customers": [
            {
                "customer_id": c.customer_id,
                "name": c.name,
                "emi": c.emi
            }
            for c in highest_emi
        ],
        "overdue_buckets": {
            "0-30": bucket_0_30,
            "31-60": bucket_31_60,
            "61-90": bucket_61_90,
            "90+": bucket_90
        }
    }