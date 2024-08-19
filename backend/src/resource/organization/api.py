from fastapi import APIRouter, Depends
from typing import Annotated

organiz_router = APIRouter()

@organiz_router.post("/create_organization",status_code=201)
def create_organization_api():
    ...


@organiz_router.get("/get_organization",status_code=200)
def get_organization_api():
    ...


@organiz_router.delete("/delete_organization",status_code=200)
def delete_organization_api():
    ...


@organiz_router.patch("/update_organization",status_code=201)
def update_organization_api():
    ...

