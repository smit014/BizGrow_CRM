from fastapi import HTTPException, Header
import jwt
from backend.src.config import Config
from backend.database.database import Sessionlocal
from backend.src.resource.user.model import User
from backend.src.utils.jwt_token import generate_access_token_from_refresh_token

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
        return token_details(user_id, token)

    except jwt.ExpiredSignatureError:

        refresh_token = Authorization.split(" ")[2]
        new_access_token = generate_access_token_from_refresh_token(refresh_token)

        decode_new_token = jwt.decode(
            new_access_token, Config.JWT_SECRET_KEY, algorithms=["HS256"]
        )
        user_id = decode_new_token.get("id")

        return token_details(user_id, new_access_token)

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


def token_details(user_id, token):
    user_data = db.query(User).filter(User.id == user_id).first()
    if user_data is None:
        raise HTTPException(status_code=401, detail="User not found")

    # if require_admin and not user_data.is_admin:
    #     raise HTTPException(status_code=403, detail="you haven't admin privileges")

    user_dict = user_data.__dict__
    user_dict.pop("_sa_instance_state", None)
    return {"access_token": token, "user_data": user_dict}
