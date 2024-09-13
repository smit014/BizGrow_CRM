from fastapi import APIRouter, Depends
from typing import Annotated
from backend.src.resource.user.schema import UserRequest,UserUpdate,AddressUpdate,subscriptionRequest
from backend.src.utils.validator import authorization
from backend.src.functionality.user.user import create_user, get_user, delete_user,update_user,update_address,create_subscription

user_router = APIRouter()


@user_router.post("/signup", status_code=201)
def create_user_api(user_data: UserRequest):
    user_info = create_user(user_data.model_dump())
    return user_info



@user_router.get("/get_user", status_code=200)
def get_user_api(user_data: Annotated[dict, Depends(authorization)]):
    user_data=user_data.get("user_data")
    user_info = get_user(user_data.get("id"),user_data)
    return user_info


@user_router.patch("/user_details", status_code=201)
def update_user_api(user_detail:UserUpdate, user_data: Annotated[dict, Depends(authorization)]):
    user_data=user_data.get("user_data")
    user_info = update_user(user_detail.model_dump(), user_data)
    return user_info


@user_router.delete("/user_details/{user_id}", status_code=204)
def delete_user_api(user_id: str, user_data: Annotated[dict, Depends(authorization)]):
    user_data=user_data.get("user_data")
    user_info = delete_user(user_id, user_data)
    return user_info

@user_router.post("/add_address",status_code=201)
def add_address_api(user_detail:AddressUpdate, user_data: Annotated[dict, Depends(authorization)]):
    user_data=user_data.get("user_data")
    user_info = update_address(user_detail.model_dump(), user_data)
    return user_info


@user_router.post("/create_subscription",status_code=201)
def create_subscription_api(user_data:subscriptionRequest):
    user_info = create_subscription(user_data.model_dump())
    return user_info