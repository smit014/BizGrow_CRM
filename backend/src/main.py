from fastapi import FastAPI
from backend.src.resource.user.api import user_router
from backend.src.resource.authentication.api import auth_router
from backend.src.resource.customer.api import customer_router
from backend.src.resource.organization.api import organization_router
from backend.src.resource.items.api import item_router
from backend.src.resource.invoice.api import invoice_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(organization_router)
app.include_router(item_router)
app.include_router(customer_router)
app.include_router(invoice_router)