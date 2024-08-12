from pydantic import BaseModel
from typing import Optional


class UserRequest(BaseModel):
    name: str
    phone_no: Optional[int]
    email: Optional[str]
    password: Optional[str]
    address: Optional[str]


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone_no: Optional[int] = None
    address: Optional[str] = None


class AddressUpdate(BaseModel):
    address: str