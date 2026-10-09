import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_device():
    response = client.post("/devices/", json={
        "name": "Smart Thermostat",
        "device_type": "HVAC",
        "firmware_version": "1.0.0",
        "ip_address": "192.168.1.100",
        "location": "Living Room",
        "owner": "Alice Smith"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Smart Thermostat"
    assert data["status"] == "offline"
    assert data["ip_address"] == "192.168.1.100"
    assert data["location"] == "Living Room"
    assert data["owner"] == "Alice Smith"
    assert "id" in data

def test_list_devices():
    response = client.get("/devices/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_and_update_device():
    # 1. Create a device
    create_response = client.post("/devices/", json={
        "name": "Smart Bulb",
        "device_type": "Lighting",
        "firmware_version": "2.1.0"
    })
    dev_id = create_response.json()["id"]

    # 2. Get the device
    get_response = client.get(f"/devices/{dev_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Smart Bulb"
    assert get_response.json()["status"] == "offline"
    assert get_response.json()["location"] is None

    # 3. Update device status
    update_response = client.put(f"/devices/{dev_id}/status", json={"status": "online"})
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "online"
    
    # 4. Update device location
    loc_response = client.put(f"/devices/{dev_id}/location", json={
        "location": "Kitchen",
        "ip_address": "10.0.0.50"
    })
    assert loc_response.status_code == 200
    assert loc_response.json()["location"] == "Kitchen"
    assert loc_response.json()["ip_address"] == "10.0.0.50"

def test_delete_device():
    # 1. Create a device
    create_response = client.post("/devices/", json={
        "name": "Security Camera",
        "device_type": "Security",
        "firmware_version": "1.0"
    })
    dev_id = create_response.json()["id"]

    # 2. Delete the device
    del_response = client.delete(f"/devices/{dev_id}")
    assert del_response.status_code == 200

    # 3. Verify deletion
    get_response = client.get(f"/devices/{dev_id}")
    assert get_response.status_code == 404
