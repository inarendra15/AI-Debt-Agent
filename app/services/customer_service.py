from app.database.database import SessionLocal
from app.database.models import Customer


def get_customer(customer_id: int):
    db = SessionLocal()

    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

    db.close()

    return customer