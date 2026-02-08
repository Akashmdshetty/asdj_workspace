import requests
import json
import os
import django

# Setup Django for DB access
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings.local')
django.setup()
from backend.core.models import ConnectionRequest, Tenant, Membership

BASE_URL = 'http://127.0.0.1:8000/api'

def test_workspace_flow():
    # 1. Login as aakashdshetty
    print("Logging in as aakashdshetty...")
    resp = requests.post(f"{BASE_URL}/auth/login/", json={
        'username': 'aakashdshetty',
        'password': 'asda3539'
    })
    
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return
        
    token = resp.json()['token']
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 2. Create Workspace
    print("\nCreating workspace 'Test Project Alpha'...")
    resp = requests.post(f"{BASE_URL}/workspaces/", headers=headers, json={
        'name': 'Test Project Alpha'
    })
    
    if resp.status_code != 201:
        print(f"Create failed: {resp.text}")
        return
        
    print("Workspace created!")
    
    # 3. List Workspaces
    resp = requests.get(f"{BASE_URL}/workspaces/", headers=headers)
    workspaces = resp.json()
    print(f"Found {len(workspaces)} workspaces.")
    my_ws = workspaces[0]
    print(f"Selected: {my_ws['name']} (ID: {my_ws['id']})")
    
    # 4. Add Member (User3 - ID 107465)
    # Ensure they are connected first (we did this in previous step)
    target_id = '107465'
    print(f"\nAdding member {target_id}...")
    resp = requests.post(f"{BASE_URL}/workspaces/{my_ws['id']}/members/", headers=headers, json={
        'unique_id': target_id
    })
    
    print(f"Add Member Status: {resp.status_code}")
    print(f"Response: {resp.text}")
    
    # 5. Verify Membership
    resp = requests.get(f"{BASE_URL}/workspaces/{my_ws['id']}/members/", headers=headers)
    members = resp.json()
    print(f"\nCurrent Members ({len(members)}):")
    for m in members:
        print(f"- {m['user']['username']} ({m['role']})")

if __name__ == "__main__":
    test_workspace_flow()
