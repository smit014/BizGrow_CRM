from database.database import Sessionlocal
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import uuid
from src.resource.customer.model import Customer
from src.resource.customer.serializer import serializer_for_customer
from src.resource.user.model import User
from src.resource.userroll.model import UserRole
from datetime import datetime


db = Sessionlocal()

def create_customer(customer_details, org_id,user_id):
    # Verify the user belongs to the organization
    user = db.query(User).filter_by(id=user_id, is_active=True, is_deleted=False).first()
    if not user:
        raise HTTPException(status_code=403, detail="User not found or not active")
    
    user_orgs = db.query(UserRole).filter_by(user_id=user_id, organization_id=org_id).first()
    if not user_orgs:
        raise HTTPException(status_code=403, detail="User does not belong to this organization")

    # Check if email exists within the same organization
    existing_customer = db.query(Customer).filter_by(
        email=customer_details.get("email"), organization_id=org_id
    ).first()
    
    if existing_customer:
        raise HTTPException(status_code=409, detail="Email is already used in this organization")

    customer_id = str(uuid.uuid4())
    
    new_customer = Customer(
        id=customer_id,
        name=customer_details.get("name"),
        email=customer_details.get("email"),
        phone=customer_details.get("phone"),
        company_name=customer_details.get("company_name"),
        bill_address=customer_details.get("bill_address"),
        city=customer_details.get("city"),
        state=customer_details.get("state"),
        pincode_no=customer_details.get("pincode"),
        organization_id=org_id,
        created_by=user_id,
        status="Active"
    )

    db.add(new_customer)
    db.commit()
    db.close()

    customer_response = {
        "id":customer_id,
        "name":customer_details.get("name"),
        "email":customer_details.get("email"),
        "phone":customer_details.get("phone"),
        "company_name":customer_details.get("company_name"),
        "bill_address":customer_details.get("bill_address"),
        "city":customer_details.get("city"),
        "state":customer_details.get("state"),
        "pincode_no":customer_details.get("pincode"),
        "organization_id":org_id,
        "created_by":user_id,
        "status":"Active"
    }

    
    return JSONResponse({"Message": "Customer created successfully", "Customer": customer_response})

def update_customer(customer_id, customer_data, org_id,user_id):
    user = db.query(User).filter_by(id=user_id, is_active=True, is_deleted=False).first()
    if not user:
        raise HTTPException(status_code=403, detail="User not found or not active")
    
    user_orgs = db.query(UserRole).filter_by(user_id=user_id, organization_id=org_id).first()
    if not user_orgs:
        raise HTTPException(status_code=403, detail="User does not belong to this organization")

    customer = db.query(Customer).filter_by(
        id=customer_id, organization_id=org_id, status="Active"
    ).first()

    if customer:
        customer.name = customer_data.get("name") if customer_data.get("name") else customer.name
        customer.email = customer_data.get("email") if customer_data.get("email") else customer.email
        customer.phone = customer_data.get("phone") if customer_data.get("phone") else customer.phone
        customer.company_name = customer_data.get("company_name") if customer_data.get("company_name") else customer.company_name
        customer.bill_address = customer_data.get("bill_address") if customer_data.get("bill_address") else customer.bill_address
        customer.city = customer_data.get("city") if customer_data.get("city") else customer.city
        customer.state = customer_data.get("state") if customer_data.get("state") else customer.state
        customer.pincode_no = customer_data.get("pincode") if customer_data.get("pincode") else customer.pincode
        customer.updated_at = datetime.now()

        db.commit()
        db.close()
        
        return JSONResponse({"Message": "Customer updated successfully"})
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


def get_customer(customer_id, org_id,user_id):
    user = db.query(User).filter_by(id=user_id, is_active=True, is_deleted=False).first()
    if not user:
        raise HTTPException(status_code=403, detail="User not found or not active")
    
    user_orgs = db.query(UserRole).filter_by(user_id=user_id, organization_id=org_id).first()
    if not user_orgs:
        raise HTTPException(status_code=403, detail="User does not belong to this organization")

    customer = db.query(Customer).filter_by(
        id=customer_id, organization_id=org_id, status="Active"
    ).first()
    
    if customer:
        filter_data = serializer_for_customer(customer)
        return JSONResponse({"Data": filter_data})
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


def get_all_customers(org_id, user_id):
    # Check if the user is active and belongs to the organization
    user = db.query(User).filter_by(id=user_id, is_active=True, is_deleted=False).first()
    if not user:
        raise HTTPException(status_code=403, detail="User not found or not active")
    
    user_orgs = db.query(UserRole).filter_by(user_id=user_id, organization_id=org_id).first()
    if not user_orgs:
        raise HTTPException(status_code=403, detail="User does not belong to this organization")

    # Retrieve all active customers for the organization
    customers = db.query(Customer).filter_by(organization_id=org_id, status="Active").all()
    
    if customers:
        # Serialize the customer data for response
        filter_data = [serializer_for_customer(customer) for customer in customers]
        return JSONResponse({"Data": filter_data})
    else:
        return JSONResponse({"Data": [], "Message": "No active customers found."})


def delete_customer(customer_id, org_id,user_id):
    user = db.query(User).filter_by(id=user_id, is_active=True, is_deleted=False).first()
    if not user:
        raise HTTPException(status_code=403, detail="User not found or not active")
    
    user_orgs = db.query(UserRole).filter_by(user_id=user_id, organization_id=org_id).first()
    if not user_orgs:
        raise HTTPException(status_code=403, detail="User does not belong to this organization")

    customer = db.query(Customer).filter_by(
        id=customer_id, organization_id=org_id, status="Active"
    ).first()

    if customer:
        customer.status = "Inactive"
        customer.updated_at = datetime.now()

        db.commit()
        db.close()
        
        return JSONResponse({"Message": "Customer inactivated successfully"})
    else:
        raise HTTPException(status_code=404, detail="Customer not found")
