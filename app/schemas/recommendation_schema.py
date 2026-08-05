from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecommendationResponse(BaseModel):
    id: int
    customer_id: int
    recommended_strategy: str
    risk_level: str
    confidence: float
    reason: str
    next_action: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)