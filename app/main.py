from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="AI Debt Collection Agent")

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "AI Debt Collection Agent Running"
    }