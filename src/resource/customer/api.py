"""
The code defines API routes for creating, updating, getting, and deleting customer data with
authorization checks.

:param org_id: The `org_id` parameter in the API routes represents the organization ID to which the
customer belongs. It is used to identify the organization context for operations related to
customers within that organization
:type org_id: str
:param customer_details: The `customer_details` parameter in the API functions represents the data
related to a customer. In the `create_customer_api` function, it is of type `CustomerCreate`, which
likely contains information required to create a new customer. In the `update_customer_api`
function, it is of type `
:type customer_details: CustomerCreate
:param user_data: The `user_data` parameter in each of the API functions is used to extract user
information such as the user's ID and organization ID from the request. This information is
typically obtained from the authorization token provided in the request headers. The
`Depends(authorization)` dependency is used to validate and extract
:type user_data: Annotated[dict, Depends(authorization)]
:return: The API endpoints in the code are returning responses based on the operations being
performed:
"""
from fastapi import APIRouter, Depends
from typing import Annotated
from src.resource.customer.schema import CustomerCreate, CustomerUpdate
from src.functionality.customer.customer import (
    create_customer, update_customer, get_customer, delete_customer,get_all_customers
)
from src.utils.validator import authorization

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

@customer_router.get("/{org_id}/customer/", status_code=200)
def get_all_customer_api(org_id: str, 
    user_data: Annotated[dict, Depends(authorization)]
):
    user_id = user_data.get("user_data").get("id")
    # org_id = user_data.get("user_data").get("organization_id")
    response = get_all_customers(org_id, user_id)
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
