from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
import uuid
import os

app = FastAPI(title="IoT Device Management API", description="Production API for IoT and Users")

# --- Subscription Plan Models ---
class PlanCreate(BaseModel):
    name: str
    price: float
    features: List[str]

class Plan(PlanCreate):
    id: str
    is_active: bool
    created_at: str

class PlanToggle(BaseModel):
    is_active: bool

# --- User Data Models ---
class UserCreate(BaseModel):
    name: str
    email: str
    plan: str = "Free" 

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    plan: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserCreate):
    id: str
    is_active: bool
    created_at: str
    recent_activity: List[str] = []

# --- Device Data Models ---
class DeviceCreate(BaseModel):
    name: str
    device_type: str
    firmware_version: str
    ip_address: Optional[str] = None
    location: Optional[str] = None
    owner: Optional[str] = None
    owner_email: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    location_permission_status: Optional[str] = None
    location_updated_at: Optional[str] = None

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    device_type: Optional[str] = None
    firmware_version: Optional[str] = None
    owner: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

class Device(DeviceCreate):
    id: str
    status: str
    last_seen: str

class StatusUpdate(BaseModel):
    status: str

# --- Lead / New Connection Data Models ---
class LeadCreate(BaseModel):
    name: str
    city: str
    address: Optional[str] = None
    pincode: str
    contact_no: str

class Lead(LeadCreate):
    id: str
    created_at: str
    status: str = "New" # New, Assigned, Completed
    assigned_to: Optional[str] = None

class LeadUpdate(BaseModel):
    assigned_to: Optional[str] = None
    status: Optional[str] = None

# --- Recharge Data Models ---
class RechargeCreate(BaseModel):
    recharge_type: str
    account_id: str
    captcha: str

class Recharge(RechargeCreate):
    id: str
    created_at: str
    status: str = "Pending"

from fastapi.encoders import jsonable_encoder
import json

# --- Databases (Persistent JSON) ---
DB_FILE = os.path.join(os.path.dirname(__file__), "database.json")

devices_db: Dict[str, Device] = {}
users_db: Dict[str, User] = {}
plans_db: Dict[str, Plan] = {}
leads_db: Dict[str, Lead] = {}
recharges_db: Dict[str, Recharge] = {}

def save_db():
    data = {
        "devices": {k: jsonable_encoder(v) for k, v in devices_db.items()},
        "users": {k: jsonable_encoder(v) for k, v in users_db.items()},
        "plans": {k: jsonable_encoder(v) for k, v in plans_db.items()},
        "leads": {k: jsonable_encoder(v) for k, v in leads_db.items()},
        "recharges": {k: jsonable_encoder(v) for k, v in recharges_db.items()}
    }
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def load_db():
    global devices_db, users_db, plans_db, leads_db, recharges_db
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            devices_db = {k: Device(**v) for k, v in data.get("devices", {}).items()}
            users_db = {k: User(**v) for k, v in data.get("users", {}).items()}
            plans_db = {k: Plan(**v) for k, v in data.get("plans", {}).items()}
            leads_db = {k: Lead(**v) for k, v in data.get("leads", {}).items()}
            recharges_db = {k: Recharge(**v) for k, v in data.get("recharges", {}).items()}
    else:
        # Pre-populate Default Subscription Plans
        plan1_id = str(uuid.uuid4())
        plan2_id = str(uuid.uuid4())
        plan3_id = str(uuid.uuid4())
        plans_db[plan1_id] = Plan(id=plan1_id, name="Free", price=0.0, features=["5 Devices Maximum", "Basic Dashboard", "Standard Support"], is_active=True, created_at=datetime.now().isoformat())
        plans_db[plan2_id] = Plan(id=plan2_id, name="Pro", price=29.99, features=["Unlimited Devices", "Real-time Telemetry", "Priority Email Support"], is_active=True, created_at=datetime.now().isoformat())
        plans_db[plan3_id] = Plan(id=plan3_id, name="Enterprise", price=199.99, features=["Dedicated Account Manager", "Custom API Access", "24/7 Phone Support"], is_active=False, created_at=datetime.now().isoformat())

        # Pre-populate a dummy user
        dummy_user_id = str(uuid.uuid4())
        users_db[dummy_user_id] = User(
            id=dummy_user_id, name="Alice Smith", email="alice@example.com", plan="Pro",
            is_active=True, created_at=datetime.now().isoformat(),
            recent_activity=["Upgraded to Pro Plan", "Account created"]
        )
        save_db()

load_db()

# --- UI & Image Routes ---
@app.get("/", include_in_schema=False)
def read_index():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"message": "UI not found, but API is running!"}

@app.get("/router.jpg", include_in_schema=False)
def get_router_image():
    img_path = os.path.join(os.path.dirname(__file__), "router.jpg")
    if os.path.exists(img_path):
        return FileResponse(img_path)
    return {"message": "Image not found"}

# --- Plan Routes ---
@app.post("/plans/", response_model=Plan, status_code=201, tags=["Plans"])
def create_plan(plan: PlanCreate):
    plan_id = str(uuid.uuid4())
    new_plan = Plan(id=plan_id, name=plan.name, price=plan.price, features=plan.features, is_active=True, created_at=datetime.now().isoformat())
    plans_db[plan_id] = new_plan
    save_db()
    return new_plan

@app.get("/plans/", response_model=List[Plan], tags=["Plans"])
def list_plans(active_only: bool = False):
    plans = list(plans_db.values())
    if active_only:
        plans = [p for p in plans if p.is_active]
    return plans

@app.put("/plans/{plan_id}", response_model=Plan, tags=["Plans"])
def update_plan_status(plan_id: str, toggle: PlanToggle):
    if plan_id not in plans_db:
        raise HTTPException(status_code=404, detail="Plan not found")
    plans_db[plan_id].is_active = toggle.is_active
    save_db()
    return plans_db[plan_id]

@app.delete("/plans/{plan_id}", tags=["Plans"])
def delete_plan(plan_id: str):
    if plan_id not in plans_db:
        raise HTTPException(status_code=404, detail="Plan not found")
    del plans_db[plan_id]
    save_db()
    return {"message": "Plan deleted successfully"}

# --- User Routes ---
@app.post("/users/", response_model=User, status_code=201, tags=["Users"])
def create_user(user: UserCreate):
    user_id = str(uuid.uuid4())
    new_user = User(id=user_id, name=user.name, email=user.email, plan=user.plan, is_active=True, created_at=datetime.now().isoformat(), recent_activity=["Account created"])
    users_db[user_id] = new_user
    save_db()
    return new_user

@app.get("/users/", response_model=List[User], tags=["Users"])
def list_users():
    return list(users_db.values())

@app.put("/users/{user_id}", response_model=User, tags=["Users"])
def update_user(user_id: str, update_data: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user = users_db[user_id]
    if update_data.name is not None: user.name = update_data.name
    if update_data.email is not None: user.email = update_data.email
    if update_data.plan is not None: user.plan = update_data.plan
    if update_data.is_active is not None: user.is_active = update_data.is_active
    save_db()
    return user

@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    save_db()
    return {"message": "User deleted successfully"}

# --- Device Routes ---
@app.post("/devices/", response_model=Device, status_code=201, tags=["Devices"])
def create_device(device: DeviceCreate):
    dev_id = str(uuid.uuid4())
    new_device = Device(id=dev_id, name=device.name, device_type=device.device_type, firmware_version=device.firmware_version, ip_address=device.ip_address, location=device.location, owner=device.owner, owner_email=device.owner_email, latitude=device.latitude, longitude=device.longitude, location_permission_status=device.location_permission_status, location_updated_at=device.location_updated_at, status="offline", last_seen=datetime.now().isoformat())
    devices_db[dev_id] = new_device
    save_db()
    return new_device

@app.get("/devices/", response_model=List[Device], tags=["Devices"])
def list_devices():
    return list(devices_db.values())

@app.put("/devices/{device_id}", response_model=Device, tags=["Devices"])
def update_device(device_id: str, update_data: DeviceUpdate):
    if device_id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")
    dev = devices_db[device_id]
    if update_data.name is not None: dev.name = update_data.name
    if update_data.device_type is not None: dev.device_type = update_data.device_type
    if update_data.firmware_version is not None: dev.firmware_version = update_data.firmware_version
    if update_data.owner is not None: dev.owner = update_data.owner
    if update_data.latitude is not None: dev.latitude = update_data.latitude
    if update_data.longitude is not None: dev.longitude = update_data.longitude
    save_db()
    return dev

@app.delete("/devices/{device_id}", tags=["Devices"])
def delete_device(device_id: str):
    if device_id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")
    del devices_db[device_id]
    save_db()
    return {"message": "Device deleted successfully"}

# --- Leads / New Connections Routes ---
@app.post("/leads/", response_model=Lead, status_code=201, tags=["Leads"])
def create_lead(lead: LeadCreate):
    lead_id = str(uuid.uuid4())
    new_lead = Lead(id=lead_id, name=lead.name, city=lead.city, address=lead.address, pincode=lead.pincode, contact_no=lead.contact_no, created_at=datetime.now().isoformat())
    leads_db[lead_id] = new_lead
    save_db()
    return new_lead

@app.get("/leads/", response_model=List[Lead], tags=["Leads"])
def list_leads():
    return list(leads_db.values())

@app.put("/leads/{lead_id}", response_model=Lead, tags=["Leads"])
def update_lead(lead_id: str, update_data: LeadUpdate):
    if lead_id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead not found")
    if update_data.assigned_to is not None:
        leads_db[lead_id].assigned_to = update_data.assigned_to
    if update_data.status is not None:
        leads_db[lead_id].status = update_data.status
    save_db()
    return leads_db[lead_id]

@app.delete("/leads/{lead_id}", tags=["Leads"])
def delete_lead(lead_id: str):
    if lead_id in leads_db:
        del leads_db[lead_id]
    save_db()
    return {"message": "Deleted"}

# --- Recharge Routes ---
@app.post("/recharges/", response_model=Recharge, status_code=201, tags=["Recharges"])
def create_recharge(req: RechargeCreate):
    r_id = str(uuid.uuid4())
    new_r = Recharge(
        id=r_id, 
        recharge_type=req.recharge_type, 
        account_id=req.account_id, 
        captcha=req.captcha, 
        created_at=datetime.now().isoformat()
    )
    recharges_db[r_id] = new_r
    save_db()
    return new_r

@app.get("/recharges/", response_model=List[Recharge], tags=["Recharges"])
def list_recharges():
    return list(recharges_db.values())

@app.delete("/recharges/{r_id}", tags=["Recharges"])
def delete_recharge(r_id: str):
    if r_id in recharges_db:
        del recharges_db[r_id]
    save_db()
    return {"message": "Deleted"}


