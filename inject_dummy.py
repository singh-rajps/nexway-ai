import json
import uuid
import random
from datetime import datetime, timedelta
import os

db_path = 'database.json'
if not os.path.exists(db_path):
    print("Database not found!")
    exit(1)

with open(db_path, 'r') as f:
    db = json.load(f)

# Ensure keys exist
for key in ['users', 'leads', 'recharges', 'devices']:
    if key not in db:
        db[key] = {}

def random_date(start_days_ago, end_days_ago):
    days = random.randint(end_days_ago, start_days_ago)
    return (datetime.now() - timedelta(days=days)).isoformat()

# Add 25 Users across the last 6 months
for i in range(25):
    uid = str(uuid.uuid4())
    db['users'][uid] = {
        "id": uid, "name": f"User {random.randint(100, 999)}", "email": f"user{random.randint(100,999)}@example.com",
        "plan": random.choice(["Free", "Pro", "Enterprise"]), "is_active": True,
        "created_at": random_date(180, 0), "recent_activity": []
    }

# Add 35 Leads across the last 6 months
for i in range(35):
    lid = str(uuid.uuid4())
    db['leads'][lid] = {
        "id": lid, "name": f"Lead {random.randint(100, 999)}", "city": random.choice(["Bangalore", "Mumbai", "Delhi", "Chennai"]),
        "address": "Random Street Area", "pincode": f"4000{random.randint(10,99)}", "contact_no": f"98765{random.randint(10000,99999)}",
        "created_at": random_date(180, 0), "status": random.choice(["New", "Assigned", "Completed"]), "assigned_to": None
    }

# Add 50 Recharges across the last 6 months
for i in range(50):
    rid = str(uuid.uuid4())
    db['recharges'][rid] = {
        "id": rid, "recharge_type": random.choice(["account", "mobile"]),
        "account_id": f"ACC{random.randint(1000,9999)}", "captcha": "X7qP9",
        "created_at": random_date(180, 0), "status": random.choice(["Pending", "Success", "Failed"])
    }

# Write back
with open(db_path, 'w') as f:
    json.dump(db, f, indent=4)

print("Dummy data successfully injected!")
