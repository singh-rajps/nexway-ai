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

if 'devices' not in db:
    db['devices'] = {}

def random_date(start_days_ago, end_days_ago):
    days = random.randint(end_days_ago, start_days_ago)
    return (datetime.now() - timedelta(days=days)).isoformat()

device_types = ["Router NX-100", "Fiber Modem V2", "Mesh Extender", "Enterprise Gateway", "Smart Hub"]
statuses = ["online", "offline", "maintenance"]

# Add 40 dummy devices
for i in range(40):
    dev_id = str(uuid.uuid4())
    is_assigned = random.choice([True, False, True]) # Higher chance of being assigned
    owner = f"User {random.randint(100, 999)}" if is_assigned else None
    
    # Approximate generic lat/lon bounds for India
    lat = round(random.uniform(12.9, 28.7), 4)
    lon = round(random.uniform(72.8, 80.2), 4)
    
    db['devices'][dev_id] = {
        "id": dev_id,
        "name": f"NX-Device-{random.randint(1000, 9999)}",
        "device_type": random.choice(device_types),
        "firmware_version": f"v{random.randint(1,4)}.{random.randint(0,9)}.{random.randint(0,9)}",
        "ip_address": f"192.168.{random.randint(0,255)}.{random.randint(1,254)}",
        "location": random.choice(["Living Room", "Office", "Bedroom", "Warehouse"]) if is_assigned else "Warehouse",
        "owner": owner,
        "owner_email": f"{owner.replace(' ', '').lower()}@example.com" if owner else None,
        "latitude": lat,
        "longitude": lon,
        "location_permission_status": "granted",
        "location_updated_at": random_date(30, 0),
        "status": random.choices(statuses, weights=[0.7, 0.2, 0.1])[0],
        "last_seen": random_date(5, 0)
    }

with open(db_path, 'w') as f:
    json.dump(db, f, indent=4)

print("Dummy devices successfully injected!")
