from decimal import Decimal
def serializer_for_customer(customer_data):
    if not isinstance(customer_data, list):
        customer_data = [customer_data]
    filter_data = {}

    for record in customer_data:
        filter_data = {
                "id": record.id,
                "name": record.name,
                "email": record.email,
                "phone": getattr(record, 'phone', ''),
                "company_name": getattr(record, 'company_name', ''),
                "bill_address": getattr(record, 'bill_address', ''),
                "city": getattr(record, 'city', ''),
                "state": getattr(record, 'state', ''),
                "pincode": getattr(record, 'pincode_no', ''),
                "organization": {
                    "org_id": record.organization_id,
                    # "org_name": record.organization_name,
                } if record.organization_id else {},
                "created_by": {
                    "user_id": record.created_by,
                    # "username": record.creator_name,
                } if record.created_by else {},
                
                "status": record.status,
                "invoices": [
                    {
                        "invoice_id": invoice.id,
                        "total_amount": float(invoice.total_amount) if isinstance(invoice.total_amount, Decimal) else invoice.total_amount,
                    }
                    for invoice in getattr(record, 'invoices', [])
                ],
            }
    return filter_data

def serializer_for_cus_name(customer_data):
    if not isinstance(customer_data, list):
        customer_data = [customer_data]
    filter_data = {}

    for record in customer_data:
        filter_data = {
                "id": record.id,
                "name": record.name,
        }
        return filter_data