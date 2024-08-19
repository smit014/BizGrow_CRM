from pydantic import BaseModel
from typing import Optional


class ItemRequest(BaseModel):
    name : str
    purchase_price : float
    sell_price : float
    description : Optional[str]=None

class UpdateItem(BaseModel):
    name : Optional[str]=None
    purchase_price : Optional[float]=None
    sell_price : Optional[float]=None
    description : Optional[str]=None

