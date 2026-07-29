import pandas as pd

from app.database.database import SessionLocal
from app.database.models import Customer


def seed_customers():
    db = SessionLocal()

    # Don't insert if customers already exist
    if db.query(Customer).first():
        print("Customers already exist.")
        db.close()
        return

    df = pd.read_csv("data/customers.csv")

    for _, row in df.iterrows():
        customer = Customer(
            customer_id=row["customer_id"],
            name=row["name"],
            loan_type=row["loan_type"],
            loan_amount=row["loan_amount"],
            emi=row["emi"],
            outstanding=row["outstanding"],
            days_overdue=row["days_overdue"],
        )

        db.add(customer)

    db.commit()
    db.close()

    print("Customer data imported successfully.")