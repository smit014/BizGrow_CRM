# from pydantic import BaseModel
# from typing import List, Optional

# class InvoiceItemRequest(BaseModel):
#     item_id: str
#     quantity: int
#     unit_price: float


# class InvoiceRequest(BaseModel):
#     invoice_date: Optional[str]  # Invoice date is optional as it may default to current date
#     customer_id: str
#     invoice_no: str
#     organization_id: str
#     user_id: str
#     items: List[InvoiceItemRequest]

# class UpdateInvoice(BaseModel):
#     invoice_date: Optional[str]
#     customer_id: Optional[str]
#     invoice_no: Optional[str]
#     items: Optional[List[InvoiceItemRequest]] = []

from pydantic import BaseModel
from typing import List

class InvoiceItemRequest(BaseModel):
    item_id: int
    quantity: int
    unit_price: float

class InvoiceRequest(BaseModel):
    invoice_no: str
    total_amount: float
    customer_id: int
    invoice_items: List[InvoiceItemRequest]

class InvoiceUpdate(BaseModel):
    invoice_no: str = None
    total_amount: float = None
