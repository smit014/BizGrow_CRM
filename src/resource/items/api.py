"""
The above code defines API routes for creating, updating, getting specific, and getting all items
with authorization checks.

:param org_id: The `org_id` parameter in the functions represents the organization ID to which the
item belongs or is associated with. It is used to identify and retrieve items specific to that
organization
:type org_id: str
:param item_details: `item_details` is a parameter that represents the details of an item that is
being created or updated. It is expected to be of type `ItemCreate` for creating a new item and
`ItemUpdate` for updating an existing item. These types likely contain specific fields and data
structures related to the
:type item_details: ItemCreate
:param user_data: The `user_data` parameter in your FastAPI endpoints is used to extract
user-specific data from the request. It seems to contain information about the user making the
request, such as their ID and organization ID. This data is extracted using the
`Depends(authorization)` dependency, which likely handles authentication
:type user_data: Annotated[dict, Depends(authorization)]
:return: The code provided defines API endpoints for item-related operations using FastAPI. The
functions defined in the code return responses based on the operations performed:
"""
from fastapi import APIRouter, Depends
from typing import Annotated
from src.resource.items.schema import ItemCreate, ItemUpdate
from src.utils.validator import authorization
from src.functionality.items.items import create_item, update_item, get_item, get_all_items

item_router = APIRouter()

# Create a new item
@item_router.post("/{org_id}/item", status_code=201)
def create_item_api(org_id: str, item_details: ItemCreate, user_data: Annotated[dict, Depends(authorization)]):
    user_id = user_data.get("user_data").get("id")
    # org_id = user_data.get("user_data").get("organization_id")
    response = create_item(item_details.model_dump(), user_id, org_id)
    return response

# Update an existing item
@item_router.patch("/{org_id}/item/{item_id}", status_code=200)
def update_item_api(org_id: str, item_id: str, item_details: ItemUpdate, user_data: Annotated[dict, Depends(authorization)]):
    user_id = user_data.get("user_data").get("id")
    # org_id = user_data.get("user_data").get("organization_id")
    response = update_item(item_id, item_details.model_dump(), user_id, org_id)
    return response

# Get a specific item by ID
@item_router.get("/{org_id}/item/{item_id}", status_code=200)
def get_item_api(org_id: str, item_id: str, user_data: Annotated[dict, Depends(authorization)]):
    # org_id = user_data.get("user_data").get("organization_id")
    user_id = user_data.get("user_data").get("id")
    response = get_item(item_id, org_id, user_id)
    return response

# Get all items for the user's organization
@item_router.get("/{org_id}/items", status_code=200)
def get_all_items_api(org_id: str, user_data: Annotated[dict, Depends(authorization)]):
    # org_id = user_data.get("user_data").get("organization_id")
    user_id = user_data.get("user_data").get("id")
    response = get_all_items(org_id, user_id)
    return response
