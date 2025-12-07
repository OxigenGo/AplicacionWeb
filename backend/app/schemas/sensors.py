from pydantic import BaseModel
from typing import Optional


class AssociationData(BaseModel):
    user_id: int
    uuid: str


class AssociationDeletionData(BaseModel):
    user_id: int
    erase_all: bool
    uuid: Optional[str]


class UserSensorList(BaseModel):
    user_id: int


class Reading(BaseModel):
    associated_uuid: str
    gas: float
    temperature: float
    position: Optional[str] = None
