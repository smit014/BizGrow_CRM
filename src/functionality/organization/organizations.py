from database.database import Sessionlocal
from src.resource.organization.model import Organization
from src.resource.organization.serializer import serializer_for_organization,serializer_for_all_org_name
from src.resource.userroll.model import UserRole
import uuid
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError


db = Sessionlocal()

def open_dashboard(org_id, user_id):
    get_organization_details(org_id, user_id)


def create_organization(org_details, user_id):
    id = str(uuid.uuid4())
    try:
        # Start a transaction
        org_info = Organization(
            id=id,
            name=org_details.get('name'),
            industry=org_details.get('industry'),
            country=org_details.get('country'),
            country_state=org_details.get('state'),
            address=org_details.get('address'),
            GST_no=org_details.get('gst_no') if org_details.get('gst_no') else None
        )
        db.add(org_info)

        # Assign the user as an admin for this organization
        user_role = UserRole(
            id=str(uuid.uuid4()),
            user_id=user_id,
            organization_id=id,
            role='Admin'  # Assign the role as Admin
        )
        db.add(user_role)

        # Commit only if both operations are successful
        db.commit()

        return JSONResponse({"Message": "Organization created successfully", "Org_id": str(id)})

    except IntegrityError as ie:
        # Handle unique constraint errors specifically
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Unique value error: {str(ie.orig)}")

    except Exception as e:
        # Rollback the transaction if any other error occurs
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    except SQLAlchemyError as e:
        # Rollback the transaction if any SQLAlchemy error occurs
        db.rollback()
        raise Exception(f"Database error: {str(e)}")

    finally:
        db.close()


def update_organization(org_id, org_details, user_id):
    try:
        # Check if the user is an admin for this organization
        user_role = db.query(UserRole).filter_by(user_id=user_id, organization_id=org_id, role='Admin').first()
        if user_role:
        # Update the organization details
            org_data = db.query(Organization).filter_by(id=org_id).first()
            if org_data:
                org_data.name = (org_details.get("name")if org_details.get("name") else org_data.name)
                org_data.industry = (org_details.get("industry") if org_details.get("industry") else org_data.industry)
                org_data.country = (org_details.get("country") if org_details.get("country") else org_data.country)
                org_data.country_state = (org_details.get("country_state") if org_details.get("country_state") else org_data.country_state)
                org_data.address = (org_details.get("address") if org_details.get("address") else org_data.address)
                org_data.updated_at = datetime.now()
                db.commit()
                return JSONResponse({"Message": "Organization updated successfully"})
            else:
                raise HTTPException(status_code=404, detail="Organization not found")
        else:
            raise HTTPException(status_code=403, detail="You do not have permission to update this organization")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        # Rollback the transaction if any SQLAlchemy error occurs
        db.rollback()
        raise Exception(f"Database error: {str(e)}")
    finally:
        db.close()


def get_organization_details(org_id, user_id):
    try:
        # Check if the user belongs to the organization
        user_role = db.query(UserRole).filter_by(user_id=user_id, organization_id=org_id).first()
        if user_role:
            org_data = db.query(Organization).filter_by(id=org_id).first()
            if org_data:
                filter_data = serializer_for_organization(org_data) 
                return JSONResponse({"Organization": filter_data})
            else:
                raise HTTPException(status_code=404, detail="Organization not found")
        else:
            raise HTTPException(status_code=403, detail="You do not have permission to view this organization")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        # Rollback the transaction if any SQLAlchemy error occurs
        db.rollback()
        raise Exception(f"Database error: {str(e)}")
    finally:
        db.close()


def delete_organization(org_id, user_id):
    try:
        # Check if the user is an admin for this organization
        user_role = db.query(UserRole).filter_by(user_id=user_id, organization_id=org_id, role='Admin').first()
        if user_role:
            org_data = db.query(Organization).filter_by(id=org_id).first()
            if org_data:
                db.delete(org_data)
                db.commit()
                return JSONResponse({"Message": "Organization deleted successfully"})
            else:
                raise HTTPException(status_code=404, detail="Organization not found")
        else:
            raise HTTPException(status_code=403, detail="You do not have permission to delete this organization")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        # Rollback the transaction if any SQLAlchemy error occurs
        db.rollback()
        raise Exception(f"Database error: {str(e)}")
    finally:
        db.close()


def list_user_organizations(user_id):
    try:
        user_roles = db.query(UserRole).filter_by(user_id=user_id).all()
        org_ids = [user_role.organization_id for user_role in user_roles]
        organizations = db.query(Organization).filter(Organization.id.in_(org_ids)).all()

        org_list = serializer_for_all_org_name(organizations)

        return JSONResponse({"Organizations": org_list})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        # Rollback the transaction if any SQLAlchemy error occurs
        db.rollback()
        raise Exception(f"Database error: {str(e)}")
    finally:
        db.close()


def assign_role_to_user(org_id, user_id, target_user_id, role):
    try:
        # Check if the user is an admin for this organization
        user_role = db.query(UserRole).filter_by(user_id=user_id, organization_id=org_id, role='Admin').first()
        if user_role:
            # Assign the role to the target user
            new_user_role = UserRole(
                id=str(uuid.uuid4()),
                user_id=target_user_id,
                organization_id=org_id,
                role=role
            )
            db.add(new_user_role)
            db.commit()
            return JSONResponse({"Message": "Role assigned successfully"})
        else:
            raise HTTPException(status_code=403, detail="You do not have permission to assign roles")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        # Rollback the transaction if any SQLAlchemy error occurs
        db.rollback()
        raise Exception(f"Database error: {str(e)}")
    finally:
        db.close()


def remove_user_from_organization(org_id, admin_user_id, target_user_id):
    try:
        # Check if the admin user is an admin for this organization
        admin_role = db.query(UserRole).filter_by(user_id=admin_user_id, organization_id=org_id, role='Admin').first()
        if admin_role:
            # Remove the target user from the organization
            target_user_role = db.query(UserRole).filter_by(user_id=target_user_id, organization_id=org_id).first()
            if target_user_role:
                db.delete(target_user_role)
                db.commit()
                return JSONResponse({"Message": "User removed from the organization successfully"})
            else:
                raise HTTPException(status_code=404, detail="User not found in the organization")
        else:
            raise HTTPException(status_code=403, detail="You do not have permission to remove users")
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        # Rollback the transaction if any SQLAlchemy error occurs
        db.rollback()
        raise Exception(f"Database error: {str(e)}")
    finally:
        db.close()
