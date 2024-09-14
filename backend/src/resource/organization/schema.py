from pydantic import BaseModel
from typing import Optional
class OrganizationCreate(BaseModel):
    name: str
    industry: str
    country: str
    state: str
    address: str
    gst_no: Optional[str]

class OrganizationUpdate(BaseModel):
    name: Optional[str]
    industry: Optional[str]
    country: Optional[str]
    state: Optional[str]
    address: Optional[str]

class RoleAssign(BaseModel):
    target_user_id: str
    role: str
