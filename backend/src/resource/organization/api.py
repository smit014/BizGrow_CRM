from fastapi import APIRouter, Depends
from typing import Annotated
from backend.src.resource.organization.schema import OrganizationCreate, OrganizationUpdate, RoleAssign
from backend.src.utils.validator import authorization
from backend.src.functionality.organization.organizations import (
    create_organization,
    update_organization,
    get_organization_details,
    delete_organization,
    list_user_organizations,
    assign_role_to_user,
    remove_user_from_organization
)

organization_router = APIRouter()

# Create an organization
@organization_router.post("/organization", status_code=201)
def create_organization_api(org_details: OrganizationCreate, user_data: Annotated[dict, Depends(authorization)]):
    user_id = user_data.get("user_data").get("id")
    response = create_organization(org_details.model_dump(), user_id)
    return response

# Update an organization
@organization_router.patch("/organization/{org_id}", status_code=200)
def update_organization_api(org_id: str,org_details: OrganizationUpdate, user_data: Annotated[dict, Depends(authorization)]):
    # org_id = user_data.get("user_data").get("organization_id")
    user_id = user_data.get("user_data").get("id")
    response = update_organization(org_id, org_details.model_dump(), user_id)
    return response

# Get organization details
@organization_router.get("/organization/{org_id}", status_code=200)
def get_organization_details_api(org_id: str,user_data: Annotated[dict, Depends(authorization)]):
    # org_id = user_data.get("user_data").get("organization_id")
    user_id = user_data.get("user_data").get("id")
    response = get_organization_details(org_id, user_id)
    return response

# Delete an organization
@organization_router.delete("/organization/{org_id}", status_code=204)
def delete_organization_api(org_id: str, user_data: Annotated[dict, Depends(authorization)]):
    user_id = user_data.get("user_data").get("id")
    response = delete_organization(org_id, user_id)
    return response

# List all organizations the user belongs to
@organization_router.get("/all_organizations", status_code=200)
def list_user_organizations_api(user_data: Annotated[dict, Depends(authorization)]):
    user_id = user_data.get("user_data").get("id")
    response = list_user_organizations(user_id)
    return response

# Assign role to a user in an organization
@organization_router.post("/organization/{org_id}/assign_role", status_code=201)
def assign_role_to_user_api(org_id: str, role_data: RoleAssign, user_data: Annotated[dict, Depends(authorization)]):
    user_id = user_data.get("user_data").get("id")
    response = assign_role_to_user(org_id, user_id, role_data.target_user_id, role_data.role)
    return response

# Remove a user from an organization
@organization_router.delete("/organization/{org_id}/remove_user/{target_user_id}", status_code=204)
def remove_user_from_organization_api(org_id: str, target_user_id: str, user_data: Annotated[dict, Depends(authorization)]):
    admin_user_id = user_data.get("user_data").get("id")
    response = remove_user_from_organization(org_id, admin_user_id, target_user_id)
    return response
