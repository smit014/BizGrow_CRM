def serializer_for_getuser(users_data,org_id):
    if not isinstance(users_data, list):
        users_data = [users_data]
    filter_data = []

    for record in users_data:
        filter_data = {
                "id": record.id,
                "name": record.name,
                "phone_no": record.phone_no,
                "email": record.email,
                "address": record.address,
                "active": record.is_active,
                "orgs": org_id,
            }

    return filter_data


def serializer_for_login(users_data):
    if not isinstance(users_data, list):
        users_data = [users_data]
    users_data = users_data[0]
    filter_data = {
        "id": users_data.id,
        "email": users_data.email,
        "phone_no": users_data.phone_no,
    }
    return filter_data
