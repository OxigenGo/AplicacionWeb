from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IncidentFilter(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    user_handled: Optional[int] = None
    state: Optional[str] = None
    submit_date_from: Optional[datetime] = None
    submit_date_to: Optional[datetime] = None

class IncidentCreate(BaseModel):
    user_id: int
    subject: str
    description: str
    user_handled: Optional[int] = None
    state: str = "OPEN"
    
class IncidentUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    user_handled: Optional[int] = None
    state: Optional[str] = None