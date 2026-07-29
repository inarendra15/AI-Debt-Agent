from app.database.database import SessionLocal
from app.database.models import User
from app.services.security_service import hash_password


def seed_users():
    db = SessionLocal()

    if db.query(User).first():
        print("Users already exist.")
        db.close()
        return

    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password=hash_password("admin123"),
        role="admin"
    )

    agent = User(
        username="agent1",
        email="agent@example.com",
        hashed_password=hash_password("agent123"),
        role="agent"
    )

    db.add(admin)
    db.add(agent)

    db.commit()
    db.close()

    print("Users seeded successfully.")