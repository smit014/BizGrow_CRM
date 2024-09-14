from pydantic import BaseModel
from typing import Optional


class ItemCreate(BaseModel):
    name: str
    description: str
    purchase_price: float
    sell_price: float

class ItemUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    purchase_price: Optional[float]
    sell_price: Optional[float]
