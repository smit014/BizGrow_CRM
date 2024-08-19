from pydantic import BaseModel
from typing import Optional

class CustomerRequest(BaseModel):
    name : str
    email : str
    phone : Optional[int]
    company_name : Optional[str]
    bill_address : Optional[str]
    city : Optional[str]
    state : Optional[str]
    pincode : Optional[int]


class UpdateCustomer(BaseModel):
    name : Optional[str]
    email : Optional[str]
    phone : Optional[int]
    company_name : Optional[str]
    bill_address : Optional[str]
    city : Optional[str]
    state : Optional[str]
    pincode : Optional[int]

class CustomerStatus(BaseModel):
    is_active : bool