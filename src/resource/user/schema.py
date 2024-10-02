from pydantic import BaseModel
from typing import Optional


class UserRequest(BaseModel):
    name: str
    phone_no: str
    email: str
    password: str
    address: Optional[str]= None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone_no: Optional[int] = None
    address: Optional[str] = None


class AddressUpdate(BaseModel):
    address: str

class subscriptionRequest(BaseModel):
    email : str