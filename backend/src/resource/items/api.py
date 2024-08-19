from fastapi import APIRouter


items_router = APIRouter()

@items_router.post("/create_item",status_code=201)
def create_item_api():
    ...


@items_router.get("/get_item",status_code=200)
def get_item_api():
    ...


@items_router.patch("/update_item",status_code=201)
def update_item_api():
    ...


@items_router.delete("/delete_item",status_code=200)
def delete_item_api():
    ...

