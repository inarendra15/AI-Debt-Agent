from pydantic import BaseModel
from datetime import datetime


class TimelineResponse(BaseModel):
    id: int
    customer_id: int
    case_id: int | None
    event_type: str
    description: str
    created_at: datetime

    class Config:
        orm_mode = True