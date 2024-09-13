def serializer_for_item(item_data):
    if not isinstance(item_data, list):
        item_data = [item_data]
    
    serialized_items = []
    
    for item in item_data:
        serialized_items.append({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "purchase_price": float(item.purchase_price),
            "sell_price": float(item.sell_price),
            "profit": float(item.profit),
            "created_by": {
                "user_id": item.creator_id,
                # "username": item.creator.name,
            },
            "updated_at": str(item.updated_at),
        })
    
    return serialized_items
