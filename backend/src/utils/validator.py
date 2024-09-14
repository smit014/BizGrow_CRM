from fastapi import HTTPException, Header
import jwt
from backend.src.config import Config
from backend.database.database import Sessionlocal
from backend.src.resource.user.model import User
from backend.src.utils.jwt_token import generate_access_token_from_refresh_token
from backend.src.resource.userroll.model import UserRole
db = Sessionlocal()


def authorization(
    Authorization =(Header(..., description="Authorization"))
):
    token = Authorization.split(" ")[1]
    try:
        decode_token = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = decode_token.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return token_details(user_id, token)# Get user details and organization role

    except jwt.ExpiredSignatureError:
        # In case of expired access token, regenerate using the refresh token
        refresh_token = Authorization.split(" ")[2]
        new_access_token = generate_access_token_from_refresh_token(refresh_token)

        decode_new_token = jwt.decode(
            new_access_token, Config.JWT_SECRET_KEY, algorithms=["HS256"]
        )
        user_id = decode_new_token.get("id")
        # Get user details and organization role for the new token
        return token_details(user_id, new_access_token)

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")

def token_details(user_id, token):
    try:
        # Fetch user details from the database
        user_data = db.query(User).filter(User.id == user_id).first()
        if user_data is None:
            raise HTTPException(status_code=401, detail="User not found")

        # Retrieve the user's organization role (if any)
        user_role = db.query(UserRole).filter(UserRole.user_id == user_id).first()

        # Prepare the response data
        user_dict = user_data.__dict__
        user_dict.pop("_sa_instance_state", None)

        # If the user has an organization role, include it; otherwise, add a message
        if user_role:
            user_dict['organization_id'] = user_role.organization_id  # Include organization ID
        else:
            user_dict['organization_message'] = "Please add an organization."

        return {
            "access_token": token,
            "user_data": user_dict
        }

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions (like 403, 401) directly
        raise http_exc

    except Exception as e:
        # Catch any other unexpected exceptions and return a generic error
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
