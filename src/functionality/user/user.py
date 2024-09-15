from database.database import Sessionlocal
from src.resource.user.model import User,Subscription
from werkzeug.security import generate_password_hash
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.resource.authentication.serializer import serializer_for_getuser
import uuid
from datetime import datetime

db = Sessionlocal()

def create_user(user_details):
    id = str(uuid.uuid4())
    if not user_details.get("email") or not user_details.get("phone_no"):
        raise HTTPException(status_code=422, detail="Add email or phone number")
    if not user_details.get("password"):
        raise HTTPException(status_code=422, detail="Password is required")
    
    existing_user = db.query(User).filter_by(email=user_details.get("email"), is_active=True).first()
    if existing_user:
        raise HTTPException(status_code=403, detail="Email is already used, Please log in or Use another Email")
    
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
    return JSONResponse({"Message": "User created successfully", "User_id": str(id)})


def get_user(user_id,user_details):
    user_data = (
        db.query(User).filter_by(id=user_id, is_active=True, is_deleted=False).first()
    )
    org_id = user_details.get("organization_id")
    
    if user_data:
        filter_data = serializer_for_getuser(user_data,org_id)
        return JSONResponse({"user": filter_data})
    else:
        raise HTTPException(status_code=404, detail="User not found")
    # org_message = user_details.get("organization_message")
    # if org_id :
    # else:
    #     raise HTTPException(status_code=401,detail="you don't have  any Organization")


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
        return JSONResponse({"Message": "User upadate successfully"})
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
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
        return JSONResponse({"Message": "Address upadate successfully"})
    else:
        raise HTTPException(status_code=404, detail="User not found")
    

def create_subscription(user_details):
    id = str(uuid.uuid4())
    existing_user = db.query(Subscription).filter_by(email=user_details.get("email")).first()
    if existing_user:
        raise HTTPException(status_code=403, detail="You alredy subscribed")
    
    subscriber = Subscription(
        id=id,
        email=user_details.get("email"),
    )
    db.add(subscriber)
    db.commit()
    db.close()
    return JSONResponse({"Message": "Subscribe successfully"})