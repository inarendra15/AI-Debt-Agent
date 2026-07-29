from math import ceil

from app.database.database import SessionLocal
from app.database.models import Customer


def get_customers(
    page: int = 1,
    limit: int = 10,
    name: str = None,
    loan_type: str = None,
    min_overdue: int = None,
    sort_by: str = None,
):
    db = SessionLocal()

    query = db.query(Customer)

    # Search by name
    if name:
        query = query.filter(
            Customer.name.ilike(f"%{name}%")
        )

    # Filter by loan type
    if loan_type:
        query = query.filter(
            Customer.loan_type == loan_type
        )

    # Filter by overdue days
    if min_overdue is not None:
        query = query.filter(
            Customer.days_overdue >= min_overdue
        )

    # Sorting
    if sort_by == "outstanding":
        query = query.order_by(
            Customer.outstanding.desc()
        )

    elif sort_by == "overdue":
        query = query.order_by(
            Customer.days_overdue.desc()
        )

    total_records = query.count()

    total_pages = (
        ceil(total_records / limit)
        if total_records > 0
        else 1
    )

    customers = (
        query
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
        "customers": customers,
    }