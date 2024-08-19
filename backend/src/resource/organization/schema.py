from pydantic import BaseModel
from typing import Optional


class OrganizationRequest(BaseModel):
    name : str
    industry : str
    country : str
    state : str
    address : Optional[str]=None
    gst_no : Optional[str] = None

class UpdateOrganization(BaseModel):
    name : Optional[str]=None
    industry : Optional[str]=None
    country : Optional[str]=None
    state : Optional[str]=None
    address : Optional[str]=None
