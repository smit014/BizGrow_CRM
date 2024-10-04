"""
The code defines API endpoints for creating, getting, updating, and deleting invoices with
authorization checks.

:param org_id: The `org_id` parameter represents the organization ID associated with the invoice
operations. It is used to identify the specific organization for which the invoice actions are being
performed
:type org_id: str
:param invoice_data: `invoice_data` is the data required to create or update an invoice. It is of
type `InvoiceCreate` for creating a new invoice and `InvoiceUpdate` for updating an existing
invoice. These types likely contain fields such as invoice number, date, items, total amount, etc
:type invoice_data: InvoiceCreate
:param user_data: The `user_data` parameter in each of the API functions is used to pass user
authentication information to the respective invoice functions. It is extracted from the request
using the `Depends(authorization)` dependency, which ensures that the user is authorized to perform
the requested action. The `user_data` contains
:type user_data: Annotated[dict, Depends(authorization)]
:return: The API endpoints in the provided code are returning `invoice_info`, which likely contains
information related to the invoice operations such as creation, retrieval, update, or deletion. The
specific content of `invoice_info` would depend on the implementation of the functions
`create_invoice`, `get_invoice`, `update_invoice`, and `delete_invoice` in the
`src.functionality.invoice.invoice` module.
"""
from fastapi import APIRouter, Depends
from typing import Annotated
from src.resource.invoice.schema import InvoiceCreate, InvoiceUpdate
from src.utils.validator import authorization
from src.functionality.invoice.invoice import create_invoice, get_invoice, delete_invoice, update_invoice,get_all_invoices

invoice_router = APIRouter()

@invoice_router.post("/{org_id}/create_invoice", status_code=201)
def create_invoice_api(org_id: str,invoice_data: InvoiceCreate, user_data: Annotated[dict, Depends(authorization)]):
    user_data = user_data.get("user_data")
    invoice_info = create_invoice(invoice_data.model_dump(), org_id, user_data)
    return invoice_info

@invoice_router.get("/{org_id}/get_invoice/{invoice_id}", status_code=200)
def get_invoice_api(org_id: str,invoice_id: str, user_data: Annotated[dict, Depends(authorization)]):
    user_data = user_data.get("user_data")
    invoice_info = get_invoice(invoice_id, org_id, user_data)
    return invoice_info

@invoice_router.get("/{org_id}/get_invoice", status_code=200)
def get_all_invoice_api(org_id: str, user_data: Annotated[dict, Depends(authorization)]):
    user_data = user_data.get("user_data")
    invoice_info = get_all_invoices(org_id, user_data)
    return invoice_info

@invoice_router.patch("/{org_id}/update_invoice/{invoice_id}", status_code=201)
def update_invoice_api(org_id: str,invoice_id: str, invoice_data: InvoiceUpdate, user_data: Annotated[dict, Depends(authorization)]):
    user_data = user_data.get("user_data")
    invoice_info = update_invoice(invoice_id, org_id, invoice_data.model_dump(), user_data)
    return invoice_info

@invoice_router.delete("/{org_id}/delete_invoice/{invoice_id}", status_code=204)
def delete_invoice_api(org_id: str,invoice_id: str, user_data: Annotated[dict, Depends(authorization)]):
    user_data = user_data.get("user_data")
    invoice_info = delete_invoice(invoice_id, org_id, user_data)
    return invoice_info
