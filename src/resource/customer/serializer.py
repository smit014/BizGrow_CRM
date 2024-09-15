def serializer_for_customer(customer_data):
    if not isinstance(customer_data, list):
        customer_data = [customer_data]
    filter_data = []

    for record in customer_data:
        filter_data.append(
            {
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
                "created_at": str(record.created_at),
                "updated_at": str(record.updated_at),
                "status": record.status,
                "invoices": [
                    {
                        "invoice_id": invoice.id,
                        "total_amount": invoice.total_amount,
                        "created_at": str(invoice.created_at),
                    }
                    for invoice in getattr(record, 'invoices', [])
                ],
            }
        )
    return filter_data
