from backend.database.database import Sessionlocal
from backend.src.resource.user.model import User
from backend.src.resource.userroll.model import UserRole
from backend.src.resource.items.model import Item
from backend.src.resource.items.serializer import serializer_for_item
import uuid
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import HTTPException


db = Sessionlocal()

def create_item(item_details, user_id, org_id):
    # Check if the user belongs to the organization
    user = db.query(UserRole).filter_by(user_id=user_id, organization_id=org_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="User not authorized to create items for this organization")

    # Create the item
    id = str(uuid.uuid4())
    new_item = Item(
        id=id,
        name=item_details.get("name"),
        description=item_details.get("description"),
        purchase_price=item_details.get("purchase_price"),
        sell_price=item_details.get("sell_price"),
        profit=item_details.get("sell_price") - item_details.get("purchase_price"),
        creator_id=user_id,
        organization_id=org_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return JSONResponse({"Message": "Item created successfully", "Item_id": str(id)})


def update_item(item_id, update_details, user_id, org_id):
    user = db.query(UserRole).filter_by(user_id=user_id, organization_id=org_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="User not authorized to update items for this organization")

    item_data = db.query(Item).filter_by(id=item_id,organization_id = org_id).first()
    if item_data:
        item_data.name = (update_details.get("name") if update_details.get("name") else item_data.name)
        item_data.description = (update_details.get("description") if update_details.get("description") else item_data.description)
        item_data.purchase_price= (update_details.get("purchase_price") if update_details.get("purchase_price") else item_data.purchase_price)
        item_data.sell_price= (update_details.get("sell_price") if update_details.get("sell_price") else item_data.sell_price)
        item_data.profit = item_data.sell_price - item_data.purchase_price
        item_data.updated_at = datetime.now()

        db.commit()
        db.refresh(item_data)
        return JSONResponse({"Message": "Item updated successfully"})

    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
def get_item(item_id, org_id, user_id):
    user = db.query(UserRole).filter_by(user_id=user_id, organization_id=org_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="User not authorized to get item form this organization")

    item = db.query(Item).filter_by(id=item_id, organization_id=org_id).first()
    if item:
        filter_data = serializer_for_item(item)
        return JSONResponse({"Data": filter_data})
    else:
        raise HTTPException(status_code=404, detail="Item not found")

def get_all_items(org_id, user_id):
    user = db.query(UserRole).filter_by(user_id=user_id, organization_id=org_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="User not authorized to get items form this organization")

    items = db.query(Item).filter_by(organization_id=org_id).all()
    if items:
        filter_data = serializer_for_item(items)
        return JSONResponse({"Data": filter_data})
    else:
        raise HTTPException(status_code=404, detail="Create your first item")

