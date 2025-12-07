from pydantic import BaseModel
from typing import Optional


class RegistrationData(BaseModel):
    username: str
    email: str
    password: str


class LoginData(BaseModel):
    username_or_email: str
    password: str


class UpdateData(BaseModel):
    username: str
    email: str
    password: Optional[str]
    profilePic: Optional[str]


class UserDeletionData(BaseModel):
    user_id: Optional[int]
    username: Optional[str]
    email: Optional[str]
