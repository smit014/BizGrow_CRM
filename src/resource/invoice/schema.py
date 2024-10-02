# The above code defines Pydantic models for creating, updating, and representing invoice data with
# item details and default status and overdue date.
from datetime import datetime
from pydantic import BaseModel
from typing import List,Optional,Dict,Union

class InvoiceItemSchema(BaseModel):
    item_id: str
    quantity: int
    unit_price: float
class InvoiceUpdate(BaseModel):
    invoice_no: str = None
    total_amount: float = None

class InvoiceBase(BaseModel):
    invoice_no: str
    customer_id: str
    invoice_data : datetime  # bill issue date 
    items: List[InvoiceItemSchema]  # List of items with product_id, quantity, unit_price
    status: Optional[str] = 'unpaid'  # Default status is 'unpaid'
    overdue_date: Optional[datetime]  # Optional, will default to 30 days from the invoice date

class InvoiceCreate(InvoiceBase):
    pass
