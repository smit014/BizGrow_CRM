def serializer_for_organization(org_data):
    if not isinstance(org_data, list):
        org_data = [org_data]
    filter_data ={}

    for record in org_data:
        filter_data ={
                "id": record.id,
                "name": record.name,
                "industry": getattr(record, 'industry', ''),
                "country": getattr(record, 'country', ''),
                "state": getattr(record, 'country_state', ''),
                "address": getattr(record, 'address', ''),
                "GST_no": getattr(record, 'GST_no', ''),
                "created_at": str(record.created_at),
                "updated_at": str(record.updated_at),
                "users": [
                    {
                        "user_id": user_role.user.id,
                        "username": user_role.user.username,
                        "role": user_role.role,
                    }
                    for user_role in getattr(record, 'users', [])
                ],
                "invoices": [
                    {
                        "invoice_id": invoice.id,
                        "total_amount": invoice.total_amount,
                        "created_at": str(invoice.created_at),
                    }
                    for invoice in getattr(record, 'invoices', [])
                ],
                "customers": [
                    {
                        "customer_id": customer.id,
                        "name": customer.name,
                        "contact": getattr(customer, 'contact_info', ''),
                    }
                    for customer in getattr(record, 'customer', [])
                ],
            }
    return filter_data


def serializer_for_all_org_name(org_data):
    if not isinstance(org_data, list):
        org_data = [org_data]
    filter_data = {}

    for record in org_data:
        filter_data ={
                "id": record.id,
                "name": record.name,
                }
    return filter_data
