from fastapi import APIRouter, Depends
from src.functionality.dashboard.dashboard import get_dashboard


dashboard_router = APIRouter()

@dashboard_router.get("/dashboard/{organization_id}")
def get_dashborad_api(organization_id:str):
    responce = get_dashboard(organization_id)
    return responce