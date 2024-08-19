from fastapi import APIRouter

customer_router = APIRouter()

@customer_router.post("/create_customer",status_code=201)
def create_customer_api():
    ...


@customer_router.get("/get_customer",status_code=200)
def get_customer_api():
    ...


@customer_router.patch("/update_customer",status_code=201)
def update_customer_api():
    ...


@customer_router.delete("/delete_customer",status_code=200)
def delete_customer_api():
    ...


@customer_router.patch("/customer_status",status_code=201)
def change_customer_status_api():
    ...
    