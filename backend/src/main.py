from fastapi import FastAPI
from backend.src.resource.user.api import user_router
from backend.src.resource.authentication.api import auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)