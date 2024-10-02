"""
The above functions are used for generating and decoding JWT tokens for user authentication and
password reset in a FastAPI application.

:param user_data: The `user_data` parameter in the `generate_token` function is a dictionary
containing user information that will be encoded into a JWT token. It typically includes data such
as user ID, username, and any other relevant information needed for authentication and authorization
:param exp: The `exp` parameter in the code represents the expiration time for a token in days or
minutes, depending on the context in which it is used. It is used to set the expiration time for the
generated token by adding a specific number of days or minutes to the current time
:return: The code snippet provided contains functions for generating tokens, decoding tokens, and
handling token-related operations for user authentication and password reset functionalities in a
FastAPI application.
"""
import jwt
from pytz import timezone
from datetime import datetime, timedelta
from src.config import Config
from src.resource.user.model import User
from fastapi import HTTPException
from database.database import Sessionlocal
from src.resource.authentication.serializer import serializer_for_login

db = Sessionlocal()
tz = timezone('Asia/Kolkata')

def generate_token(user_data, exp):
    expires_delta = timedelta(days=int(exp))
    user_data["exp"] = datetime.now(tz) + expires_delta
    data = user_data
    encode_data = jwt.encode(data, Config.JWT_SECRET_KEY, algorithm=Config.ALGORITHM)
    return encode_data


def generate_access_token_from_refresh_token(refresh_token):
    try:
        decoded_token = jwt.decode(
            refresh_token, Config.JWT_SECRET_KEY, algorithms=[Config.ALGORITHM]
        )
        user_id = decoded_token.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_data = db.query(User).filter(User.id == user_id).first()
        if user_data is None:
            raise HTTPException(status_code=401, detail="User not found")

        filter_data = serializer_for_login(user_data)
        access_token = generate_token(
            filter_data, exp=Config.ACCESS_TOKEN_EXPIRE_DAYS
        )
        return access_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def create_reset_password_token(data):
    expires_delta = timedelta(minutes=int(Config.FORGET_PASSWORD_LINK_EXPIRE_MINUTES))
    data["exp"] = datetime.now(tz) + expires_delta
    token = jwt.encode(data, Config.FORGET_PWD_SECRET_KEY, Config.ALGORITHM)
    return token

def decode_reset_password_token(token):
    try:
        payload = jwt.decode(token, Config.FORGET_PWD_SECRET_KEY,algorithms=[Config.ALGORITHM])
        email = payload.get("email")
        return email
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")