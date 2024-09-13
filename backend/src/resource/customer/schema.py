from pydantic import BaseModel, EmailStr
from typing import Optional

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    company_name: str
    bill_address: str
    city: str
    state: str
    pincode: str


class CustomerUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    company_name: Optional[str]
    bill_address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[str]


class CustomerStatus(BaseModel):
    is_active : bool