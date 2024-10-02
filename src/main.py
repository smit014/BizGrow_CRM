# This Python code snippet is setting up a FastAPI application with multiple routers for different
# resources and enabling CORS (Cross-Origin Resource Sharing) middleware to allow cross-origin
# requests. Here's a breakdown of what each part of the code is doing:
from fastapi import FastAPI
from src.resource.user.api import user_router
from src.resource.authentication.api import auth_router
from src.resource.customer.api import customer_router
from src.resource.organization.api import organization_router
from src.resource.items.api import item_router
from src.resource.invoice.api import invoice_router
from src.resource.dashboard.api import dashboard_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:5173",  # Add your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(organization_router)
app.include_router(item_router)
app.include_router(customer_router)
app.include_router(invoice_router)
app.include_router(dashboard_router)