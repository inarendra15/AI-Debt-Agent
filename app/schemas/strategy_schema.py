from pydantic import BaseModel


class StrategyResponse(BaseModel):
    recommended_strategy: str
    risk_level: str
    confidence: int
    reason: str
    next_action: str