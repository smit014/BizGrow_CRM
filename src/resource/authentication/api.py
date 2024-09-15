"""
The code defines API routes for user authentication functionalities like login, password change,
password reset link, and password reset.

:param user_data: The `user_data` parameter in each of the API endpoints represents the data being
sent in the request body. It is of a specific type defined by the corresponding schema classes
(`UserLoginRequest`, `ChangePasswordRequest`, `PasswordResetRequest`, `ResetForegetPassword`). These
schema classes likely define
:type user_data: UserLoginRequest
:return: The functions in the code are returning user information or details related to the
authentication process.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Form
from src.utils.validator import authorization
from src.functionality.authentication.auth import (
    login_user,
    change_password,
    reset_pass_mail,
    reset_password,
)
from src.resource.authentication.schema import (
    UserLoginRequest,
    ChangePasswordRequest,
    PasswordResetRequest,
    ResetForegetPassword,
)

auth_router = APIRouter()


@auth_router.post("/login", status_code=201)
def login_api(user_data: UserLoginRequest):
    user_info = login_user(user_data.model_dump())
    return user_info


@auth_router.post("/change_password", status_code=201)
def change_password_api(
    user_data: ChangePasswordRequest,
    user_details: Annotated[dict, Depends(authorization)]
):
    user_details = user_details.get("user_data")
    user_info = change_password(user_data.model_dump(), user_details.get("id"))
    return user_info


@auth_router.post("/reset_pass_link", status_code=201)
def reset_pass_link_api(
    user_data: PasswordResetRequest,
    user_details: Annotated[dict, Depends(authorization)],
):
    user_details = user_details.get("user_data")
    user_info = reset_pass_mail(user_data.model_dump(), user_details)
    return user_info


@auth_router.post("/reset_password", status_code=201)
def reset_password_api(user_data: ResetForegetPassword):
    user_info = reset_password(user_data.model_dump())
    return user_info
