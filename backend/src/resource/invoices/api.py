from fastapi import APIRouter


invoice_router = APIRouter()

@invoice_router.post("/create_invoice",status_code=201)
def create_invoice_api():
    ...


@invoice_router.get("/get_invoice",status_code=200)
def get_invoice_api():
    ...


@invoice_router.patch("/update_invoice",status_code=201)
def update_invoice_api():
    ...


@invoice_router.delete("/delete_invoice",status_code=200)
def delete_invoice_api():
    ...

