from fastapi import FastAPI

from app.api.routes import router

from app.database.database import Base, engine
from app.database import models
from app.database.seed_database import seed_customers

# Create all database tables
Base.metadata.create_all(bind=engine)
seed_customers()

app = FastAPI(
    title="AI Debt Collection Agent"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "AI Debt Collection Agent API is running!"
    }