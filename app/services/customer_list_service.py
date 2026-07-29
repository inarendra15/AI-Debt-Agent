from math import ceil

from app.database.database import SessionLocal
from app.database.models import Customer


def get_customers(
    page: int = 1,
    limit: int = 10
):
    db = SessionLocal()

    total_records = db.query(Customer).count()

    total_pages = ceil(total_records / limit)

    customers = (
        db.query(Customer)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    db.close()

    return {
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
        "customers": customers
    }