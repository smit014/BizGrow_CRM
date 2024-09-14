from backend.database.database import Sessionlocal
from backend.src.resource.user.model import User
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from backend.src.resource.authentication.serializer import serializer_for_login
from backend.src.utils.jwt_token import (
    generate_token,
    create_reset_password_token,
    decode_reset_password_token,
)
from backend.src.utils.email_sender import sending_email
from backend.src.config import Config
from datetime import datetime

db = Sessionlocal()


def login_user(user_details):
    email = user_details.get("email")
    phone_no = user_details.get("phone_no")
    password = user_details.get("password")

    if email or phone_no:
        user_data = (
            db.query(User)
            .filter(
                or_((User.email == email), (User.phone_no == phone_no)),
                User.is_active == True,
                User.is_deleted == False,
            )
            .first()
        )
        if user_data:
            if check_password_hash(user_data.password, password):
                filtered_data = serializer_for_login(user_data)
                access_token = generate_token(
                    filtered_data, Config.ACCESS_TOKEN_EXPIRE_DAYS
                )
                refresh_token = generate_token(
                    filtered_data, Config.REFRESH_TOKEN_EXPIRE_DAYS
                )
                db.commit()
                db.close()
                return JSONResponse(
                    {"Access_Token": access_token, "Refresh_token": refresh_token},
                    status_code=200,
                )
            else:
                raise HTTPException(status_code=401, detail="Incorrect password")
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="Email or phone number is required")


def change_password(user_details, user_id):
    password = user_details.get("password")
    new_password = generate_password_hash(user_details.get("new_password"))

    user_data = None
    if user_id:
        user_data = (
            db.query(User)
            .filter_by(id=user_id, is_active=True, is_deleted=False)
            .first()
        )
        if user_data:
            if password == user_details.get("new_password"):
                raise HTTPException(
                    status_code=409,
                    detail="Old Password and New Password has to be Different",
                )
            else:
                if check_password_hash(user_data.password, password):
                    user_data.password = new_password
                    user_data.updated_at = datetime.now()
                    db.commit()
                    db.close()
                    return JSONResponse(
                        {"Message": "password successfully changed"}, status_code=200
                    )
                else:
                    raise HTTPException(
                        status_code=401, detail="Incorrect Old password"
                    )
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=407, detail="Login with correct user data")


# Send email with reset link
def reset_pass_mail(user_detail, user_data):
    if user_detail.get("email") == user_data.get("email"):
        data = {}
        data["email"] = user_data.get("email")
        secret_token = create_reset_password_token(data)
        forget_url_link = f"{Config.FORGET_PASSWORD_LINK}/{secret_token}"

        receiver_email = user_detail.get("email")
        subject = "Reset Your Password"
        body = f"Click the link below to reset your password:\n\n{forget_url_link}"
        mail = sending_email(receiver_email, subject, body)
        return mail
    else:
        raise HTTPException(status_code=401, detail="wrong email")


def reset_password(user_data):
    try:
        email_info = decode_reset_password_token(token=user_data.get("secret_token"))
        if email_info is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid Password Reset Payload or Reset Link Expired",
            )
        if user_data.get("new_password") != user_data.get("confirm_password"):
            raise HTTPException(
                status_code=409,
                detail="New password and confirm password are not same.",
            )

        hashed_password = generate_password_hash(user_data.get("new_password"))
        user = (
            db.query(User)
            .filter_by(email=email_info, is_active=True, is_deleted=False)
            .first()
        )
        user.password = hashed_password
        user.updated_at = datetime.now()
        db.commit()
        return JSONResponse(
            {"Message": "password successfully changed"}, status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Some thing unexpected happened!")
