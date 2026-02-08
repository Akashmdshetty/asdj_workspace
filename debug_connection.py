import requests
import json
import os
import django

# Setup Django for DB access
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings.local')
django.setup()
from backend.core.models import ConnectionRequest

BASE_URL = 'http://127.0.0.1:8000/api'

def debug_flow():
    # 1. Login
    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/auth/login/", json={
        'username': 'aakashdshetty',
        'password': 'asda3539'
    })
    
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return
        
    token = resp.json()['token']
    print(f"Got token: {token[:10]}...")
    
    # 2. Send Request
    target_id = '107465' # user3
    print(f"Sending request to {target_id}...")
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    resp = requests.post(f"{BASE_URL}/connections/send/", headers=headers, json={
        'unique_id': target_id
    })
    
    print(f"Response Status: {resp.status_code}")
    if resp.status_code != 201:
        print(f"Response Body Preview: {resp.text[:500]}")
    else:
        print(f"Response Body: {resp.json()}")
    
    # 3. Check DB
    print("\n--- DB Check ---")
    reqs = ConnectionRequest.objects.all()
    print(f"Total Requests: {len(reqs)}")
    for r in reqs:
        print(f"{r.sender} -> {r.receiver} ({r.status})")

if __name__ == "__main__":
    debug_flow()
