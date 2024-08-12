from backend.database.database import Sessionlocal
from backend.src.resource.user.model import User
from werkzeug.security import generate_password_hash
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from backend.src.resource.authentication.serializer import serializer_for_getuser
import uuid
from datetime import datetime

db = Sessionlocal()

def create_user(user_details):
    id = str(uuid.uuid4())
    if not user_details.get("email") or not user_details.get("phone_no"):
        raise HTTPException(status_code=422, detail="Add email or phone number")
    if not user_details.get("password"):
        raise HTTPException(status_code=422, detail="Password is required")
    user_data = db.query(User).filter_by(email = user_details.get("email"),is_active =True).first()
    if user_data:
        raise HTTPException(statusCode = 403 ,detail="email is alredy used")
    user_info = User(
        id=id,
        name=user_details.get("name"),
        email=user_details.get("email"),
        phone_no=user_details.get("phone_no"),
        password=generate_password_hash(user_details.get("password")),
    )
    db.add(user_info)
    db.commit()
    db.close()
    return {"Message": "User created successfully", "User_id": str(id)}


def get_user(user_id):
    user_data = (
        db.query(User).filter_by(id=user_id, is_active=True, is_deleted=False).first()
    )
    if user_data:
        filter_data = serializer_for_getuser(user_data)
        return JSONResponse({"Data": filter_data})
    else:
        raise HTTPException(status_code=404, detail="User not found")


def delete_user(user_id, user_details):
    if user_id == user_details.get("id"):
        user_data = (
            db.query(User)
            .filter_by(id=user_id, is_active=True, is_deleted=False)
            .first()
        )
        if user_data:
            user_data.is_active = False
            user_data.is_deleted = True
            user_data.updated_at = datetime.now()
            db.commit()
            db.close()
            return JSONResponse({"Message": "User deleted successfully"})
    else:
        raise HTTPException(status_code=409, detail="Invalid user id")


def update_user(user_data, user_id):
    user = (
        db.query(User)
        .filter_by(id=user_id.get("id"), is_active=True, is_deleted=False)
        .first()
    )
    if user:
        user.name = (
            user_data.get("name")
            if user_data.get("name") is not None
            else user.name
        )
        user.phone_no = (
            user_data.get("phone_no")
            if user_data.get("phone_no") is not None
            else user.phone_no
        )
        user.address = (
            user_data.get("address")
            if user_data.get("address") is not None
            else user.address
        )
        user.updated_at = datetime.now()
        db.commit()
        db.close()
        return JSONResponse({"Message": "user upadate successfully"})
    else:
        raise HTTPException(status_code=404, detail="user not found")
    
def update_address(user_data, user_id):
    user = (
        db.query(User)
        .filter_by(id=user_id.get("id"), is_active=True, is_deleted=False)
        .first()
    )
    if user:
        user.address = user_data.get("address")
        user.updated_at = datetime.now()
        db.commit()
        db.close()
        return JSONResponse({"Message": "address upadate successfully"})
    else:
        raise HTTPException(status_code=404, detail="user not found")