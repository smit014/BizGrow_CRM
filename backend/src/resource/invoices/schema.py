from pydantic import BaseModel
from typing import Optional


class InvoiceRequest(BaseModel):
    invoice_date = str
    customer_id  = str
    invoice_no = str
    # oraganization_id = str
    # user_id = str

class UpdateInvoice(BaseModel):
    invoice_date = str
    customer_id  = str
    invoice_no = str

