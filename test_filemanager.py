import requests
import json
import os
import django

# Setup Django for DB access
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings.local')
django.setup()
from backend.core.models import Tenant

BASE_URL = 'http://127.0.0.1:8000/api'

def test_file_manager():
    # 1. Login
    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/auth/login/", json={
        'username': 'aakashdshetty',
        'password': 'asda3539'
    })
    token = resp.json()['token']
    headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
    
    # Get Workspace
    ws = Tenant.objects.filter(owner__username='aakashdshetty').first()
    if not ws:
        print("No workspace found. Run previous test first.")
        return
    print(f"Using workspace: {ws.name} ({ws.id})")
    
    # 2. Create Root Folder "Marketing"
    print("\nCreating 'Marketing' folder...")
    resp = requests.post(f"{BASE_URL}/workspaces/{ws.id}/content/", headers=headers, json={
        'type': 'folder',
        'name': 'Marketing'
    })
    print(resp.status_code, resp.json())
    marketing_id = resp.json()['id']
    
    # 3. Create Subfolder "Q1" inside Marketing
    print("\nCreating 'Q1' subfolder...")
    resp = requests.post(f"{BASE_URL}/workspaces/{ws.id}/content/", headers=headers, json={
        'type': 'folder',
        'name': 'Q1',
        'parent_id': marketing_id
    })
    print(resp.status_code, resp.json())
    q1_id = resp.json()['id']
    
    # 4. Create File "Strategy.txt" inside Q1
    print("\nCreating 'Strategy.txt' file in Q1...")
    resp = requests.post(f"{BASE_URL}/workspaces/{ws.id}/content/", headers=headers, json={
        'type': 'file',
        'title': 'Strategy.txt',
        'parent_id': q1_id
    })
    print(resp.status_code, resp.json())
    
    # 5. List Q1 Content
    print("\nListing Q1 Content...")
    resp = requests.get(f"{BASE_URL}/workspaces/{ws.id}/content/?folder_id={q1_id}", headers=headers)
    data = resp.json()
    print("Folders:", [f['name'] for f in data['folders']])
    print("Files:", [d['title'] for d in data['documents']])
    
    if len(data['documents']) > 0 and data['documents'][0]['title'] == 'Strategy.txt':
        print("\nSUCCESS: File Manager hierarchy works!")
    else:
        print("\nFAILURE: File not found in subfolder.")

if __name__ == "__main__":
    test_file_manager()
