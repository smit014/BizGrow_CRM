from fastapi import APIRouter, Depends
from typing import Annotated
from backend.src.resource.customer.schema import CustomerCreate, CustomerUpdate
from backend.src.functionality.customer.customer import (
    create_customer, update_customer, get_customer, delete_customer
)
from backend.src.utils.validator import authorization

customer_router = APIRouter()

# Create a new customer
@customer_router.post("/{org_id}/customer", status_code=201)
def create_customer_api(org_id: str, 
    customer_details: CustomerCreate, 
    user_data: Annotated[dict, Depends(authorization)]
):
    user_id = user_data.get("user_data").get("id")
    # org_id = user_data.get("user_data").get("organization_id")
    response = create_customer(customer_details.model_dump(), org_id, user_id)
    return response

# Update an existing customer
@customer_router.patch("/{org_id}/customer/{customer_id}", status_code=200)
def update_customer_api(org_id: str, 
    customer_id: str, 
    customer_details: CustomerUpdate, 
    user_data: Annotated[dict, Depends(authorization)]
):
    user_id = user_data.get("user_data").get("id")
    # org_id = user_data.get("user_data").get("organization_id")
    response = update_customer(customer_id, customer_details.model_dump(), org_id, user_id)
    return response

# Get a customer by ID
@customer_router.get("/{org_id}/customer/{customer_id}", status_code=200)
def get_customer_api(org_id: str, 
    customer_id: str, 
    user_data: Annotated[dict, Depends(authorization)]
):
    user_id = user_data.get("user_data").get("id")
    # org_id = user_data.get("user_data").get("organization_id")
    response = get_customer(customer_id, org_id, user_id)
    return response

# Delete a customer (soft delete by setting status to Inactive)
@customer_router.delete("/{org_id}/customer/{customer_id}", status_code=200)
def delete_customer_api(org_id: str, 
    customer_id: str, 
    user_data: Annotated[dict, Depends(authorization)]
):
    user_id = user_data.get("user_data").get("id")
    # org_id = user_data.get("user_data").get("organization_id")
    response = delete_customer(customer_id, org_id, user_id)
    return response
