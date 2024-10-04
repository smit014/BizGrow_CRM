from decimal import Decimal

def serializer_for_invoice(invoice_data):
    if not isinstance(invoice_data, list):
        invoice_data = [invoice_data]
    
    filter_data = {}

    for record in invoice_data:
        filter_data ={
                "id": record.id,
                "invoice_no": record.invoice_no,
                "total_amount": float(record.total_amount) if isinstance(record.total_amount, Decimal) else record.total_amount,  # Convert Decimal to float
                "invoice_date": str(record.invoice_date),  # Convert to string for consistent formatting
                "overdue_date": str(record.overdue_date), 
                "customer_id": record.customer_id,
                "organization_id": record.organization_id,
                "created_at": str(record.created_at),
                "updated_at": str(record.updated_at),
                "status": record.status,
                "items": [
                    {
                        "item_id": item.id,
                        "quantity": item.quantity,
                        "total_price": float(item.total_price) if isinstance(item.total_price, Decimal) else item.total_price,  # Convert item price from Decimal to float
                    }
                    for item in getattr(record, 'items', [])
                ],
            }
    return filter_data
