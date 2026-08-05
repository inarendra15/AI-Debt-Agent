from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TimelineResponse(BaseModel):
    id: int
    customer_id: int
    case_id: int | None
    event_type: str
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)