from datetime import datetime, timedelta
import random
import uuid

# Customer IDs
customer_ids = [
    "0c06edf1-4538-49fc-8cdc-9fc5a395234c", "21fcf783-0646-4241-8db9-c071fb6c29f0", "dc1b2b76-62b3-4fe6-b370-57b632c6e0f6",
    "17995d13-4b6c-481f-8314-2d4c14002819", "bc95b374-8fe2-4e43-b400-24ffa63030fe", "848cfc7c-4214-4aa3-994c-536b3b32bbbc",
    "535b2461-f17f-4130-a5ec-f3620250af70", "9a9762aa-2aad-4d7d-8c1d-c1946d5427f5", "78b27105-343d-41af-ae38-be958a58955e",
    "0f91f263-c150-4bcc-b26b-d291a09e0524", "62e57d4a-445a-4045-88d8-c078c51dce0d", "f47afe93-63e2-461b-9c63-35eb22d5b486",
    "8c979ddb-90a8-4397-8472-14bee2ce928b", "92e248ed-b859-4725-959e-2e5d844519a6", "0c63a217-790c-4b8d-822a-89c6bbfcaf43",
    "f19dac41-f32d-49b3-95f2-3b03ee5754ac", "8ca429c4-b085-4ba9-8b78-fe304086b8d4", "18cbb040-2da4-4c7a-aed5-683efa8e0f79",
    "768f09bf-477b-4e24-b2d8-6865398d6de6", "894c4716-8e19-4487-b600-8b243ce61aa0", "0962a2fe-ec59-4817-9370-7be0221e70b8",
    "f3e59b45-f57c-4946-b1b7-df7dbb8ff816", "2f12a113-3bd8-4473-a85b-c31a0415fe66", "189e3fc8-83e2-425f-9128-574db5726716",
    "212ffccc-315c-48ad-abba-12f855b5eafd", "7a24a1fc-a5d3-4afd-94f6-6dfa6cbeb92c", "af6a719c-818e-47de-81ac-9c64de8f1b1d",
    "a6cb7ec9-d053-4de6-a4d2-20738ffb67d3", "f9e176d5-f908-4161-9545-42a79c112faa", "8106a837-94fc-4907-aab7-a82728996832",
    "6b93e55a-1af1-44b7-98ce-6e58ff1aaa25", "6789883e-38b4-4b1f-914b-cb4ae8ce4412", "3042f9e3-5feb-49a2-842c-e31dbc9bdd91",
    "1cd0fae3-d018-439e-abf7-0ec2b3bf97c8", "50676d3e-f888-4dd0-a0b4-87668c4d99a7", "b83e86ee-0f34-4cc3-84d7-4031c36e317d",
    "2529d30b-30b3-431e-b27a-10fb306ddc12", "fca61180-291b-4a4d-929d-da7d25215fc0", "2c421b9b-b1bb-4c3c-84dd-a751278cf2e0"
]

items = [
    {"item_id": "9c1959e4-57bb-40df-87f2-1e162b4548c5", "unit_price": 21000.00},
    {"item_id": "901bec95-5c8c-4efc-ae09-c51fa251e087", "unit_price": 48900.00},
    {"item_id": "6e26a4d9-931e-4cae-99ed-7664d4f10bb6", "unit_price": 72500.00},
    {"item_id": "981326f8-1f1d-4202-a7a9-91b1327aa7b0", "unit_price": 110000.00},
    {"item_id": "02c5dfd0-11b8-4bb7-b87b-cd6ceb9ded55", "unit_price": 12000.00},
    {"item_id": "8adba214-4321-4ad7-8b84-2b9f0979e312", "unit_price": 8500.00},
    {"item_id": "585f7256-3e12-49eb-8861-2086af626a62", "unit_price": 45000.00},
    {"item_id": "0eec02a4-2b00-45a8-9216-fe0327c8e8c7", "unit_price": 31000.00},
    {"item_id": "347dd18b-817f-4b00-99eb-8350e2d4b40e", "unit_price": 12500.00},
    {"item_id": "8e7fba09-02ae-481f-996e-0fb0656d5555", "unit_price": 34500.00},
    {"item_id": "dc1e1e6c-826c-4273-ba35-a134a1eb1864", "unit_price": 50900.00},
    {"item_id": "5cdf75d4-b486-4e5f-a04a-43c20cd6411d", "unit_price": 85000.00},
    {"item_id": "7b4b0d82-f152-4246-9d2e-744c9b8d73f5", "unit_price": 9000.00},
    {"item_id": "52f30aa4-19d0-499d-9973-41f64eed9839", "unit_price": 6500.00},
    {"item_id": "aaac7f03-d733-4b30-addd-949531f918fc", "unit_price": 22500.00},
    {"item_id": "892918bd-fdbe-4d9a-a878-7e93cc70e48d", "unit_price": 34000.00},
    {"item_id": "581c5a61-e78f-4102-b432-317363fee04e", "unit_price": 29000.00},
    {"item_id": "1dcd30db-09e6-4b0c-bb88-2f5d874ff0b2", "unit_price": 18500.00},
    {"item_id": "7db7d5e5-665c-437a-bf5d-224f8fcf88a6", "unit_price": 45000.00},
    {"item_id": "cfdc7e10-72c4-4fd2-aba2-711b732ad020", "unit_price": 120000.00},
    {"item_id": "e84eaeef-66dc-493e-8946-9743f2e1a795", "unit_price": 8500.00},
    {"item_id": "df7307e0-7a62-448f-bcad-52073832cdcf", "unit_price": 48000.00},
    {"item_id": "eafda6b6-dad6-4e1f-8101-08e85acbecd3", "unit_price": 19500.00},
    {"item_id": "5d87c410-be84-430f-a92f-445fa2948ba4", "unit_price": 65000.00},
    {"item_id": "ea854827-9b78-4190-9610-be32aa8a8ecf", "unit_price": 125000.00},
    {"item_id": "e9a323c7-8722-4d29-ab3c-589838474151", "unit_price": 7500.00}
]

def random_date(start, end):
    time_between_dates = end - start
    random_number_of_days = random.randint(0, time_between_dates.days)
    return start + timedelta(days=random_number_of_days)

# Generate random invoice data
def generate_invoice_data(n):
    start_date = datetime(2021, 3, 30)  # Start date
    end_date = datetime(2024, 3, 1)     # End date
    
    invoice_data = []
    for _ in range(n):
        invoice = {
            "customer_id": random.choice(customer_ids),
            "invoice_date": random_date(start_date, end_date).isoformat(),  # Generate random date in range
            "items": [
                {
                    "item_id": item["item_id"],
                    "quantity": random.randint(5, 20),
                    "unit_price": item["unit_price"]
                }
                for item in random.sample(items, random.randint(1, 5))  # Random number of items
            ],
            "status": random.choice(["paid", "unpaid"]),
            "overdue_date": (datetime.now() + timedelta(days=random.randint(-30, 30))).isoformat()
        }
        invoice_data.append(invoice)
    return invoice_data

invoice = generate_invoice_data(10)
print(invoice) 