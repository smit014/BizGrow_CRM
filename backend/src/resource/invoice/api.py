from fastapi import APIRouter, Depends
from typing import Annotated
from backend.src.resource.invoice.schema import InvoiceRequest, InvoiceUpdate
from backend.src.utils.validator import authorization
from backend.src.functionality.invoice.invoice import create_invoice, get_invoice, delete_invoice, update_invoice

invoice_router = APIRouter()

@invoice_router.post("/create_invoice", status_code=201)
def create_invoice_api(invoice_data: InvoiceRequest, user_data: Annotated[dict, Depends(authorization)]):
    user_data = user_data.get("user_data")
    invoice_info = create_invoice(invoice_data.model_dump(), user_data)
    return invoice_info

@invoice_router.get("/get_invoice/{invoice_id}", status_code=200)
def get_invoice_api(invoice_id: str, user_data: Annotated[dict, Depends(authorization)]):
    user_data = user_data.get("user_data")
    invoice_info = get_invoice(invoice_id, user_data)
    return invoice_info

@invoice_router.patch("/update_invoice/{invoice_id}", status_code=201)
def update_invoice_api(invoice_id: str, invoice_data: InvoiceUpdate, user_data: Annotated[dict, Depends(authorization)]):
    user_data = user_data.get("user_data")
    invoice_info = update_invoice(invoice_id, invoice_data.model_dump(), user_data)
    return invoice_info

@invoice_router.delete("/delete_invoice/{invoice_id}", status_code=204)
def delete_invoice_api(invoice_id: str, user_data: Annotated[dict, Depends(authorization)]):
    user_data = user_data.get("user_data")
    invoice_info = delete_invoice(invoice_id, user_data)
    return invoice_info
