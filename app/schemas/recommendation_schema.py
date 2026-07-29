from datetime import datetime

from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    id: int
    customer_id: int
    recommended_strategy: str
    risk_level: str
    confidence: int
    reason: str
    next_action: str
    created_at: datetime

    class Config:
        orm_mode = True