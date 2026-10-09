with open('main.py', 'r') as f:
    text = f.read()

replacements = {
    'return new_plan': 'save_db()\n    return new_plan',
    'return new_user': 'save_db()\n    return new_user',
    'return {"message": "User deleted successfully"}': 'save_db()\n    return {"message": "User deleted successfully"}',
    'return new_device': 'save_db()\n    return new_device',
    'return {"message": "Device deleted successfully"}': 'save_db()\n    return {"message": "Device deleted successfully"}',
    'return new_lead': 'save_db()\n    return new_lead',
    'return leads_db[lead_id]': 'save_db()\n    return leads_db[lead_id]',
    'return {"message": "Deleted"}': 'save_db()\n    return {"message": "Deleted"}',
    'return new_r': 'save_db()\n    return new_r',
}

for k, v in replacements.items():
    text = text.replace(k, v)

with open('main.py', 'w') as f:
    f.write(text)
