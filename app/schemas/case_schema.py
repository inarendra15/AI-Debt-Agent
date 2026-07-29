from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CaseCreate(BaseModel):
    customer_id: int
    assigned_agent: Optional[str] = None
    priority: str = "MEDIUM"


class CaseUpdate(BaseModel):
    status: Optional[str] = None
    assigned_agent: Optional[str] = None
    priority: Optional[str] = None
    next_followup: Optional[datetime] = None


class CaseResponse(BaseModel):
    id: int
    customer_id: int
    assigned_agent: Optional[str]
    status: str
    priority: str
    next_followup: Optional[datetime]

    class Config:
        from_attributes = True