from fastapi import APIRouter, Depends
from typing import Annotated
from backend.src.resource.items.schema import ItemCreate, ItemUpdate
from backend.src.utils.validator import authorization
from backend.src.functionality.items.items import create_item, update_item, get_item, get_all_items

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
