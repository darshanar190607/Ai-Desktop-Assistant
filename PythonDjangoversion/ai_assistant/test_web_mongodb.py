#!/usr/bin/env python
import os
import sys
import django
import requests
import json
from urllib.parse import urlencode

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_assistant.settings')
django.setup()

from assistant.mongodb_utils import get_mongodb_collection

def test_web_interface_mongodb():
    print("Testing Web Interface MongoDB Integration...")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    
    # Get initial count
    collection = get_mongodb_collection()
    initial_count = collection.count_documents({})
    print(f"Initial document count: {initial_count}")
    
    # Test 1: Check MongoDB connection endpoint
    print("\n1. Testing MongoDB connection endpoint...")
    try:
        response = requests.get(f"{base_url}/check-mongodb/", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
        print("   Make sure Django server is running on port 8000")
        return
    
    # Test 2: Test process input endpoint (this should save to MongoDB)
    print("\n2. Testing process input endpoint...")
    try:
        params = {'text': 'test web interface mongodb'}
        response = requests.get(f"{base_url}/process/?{urlencode(params)}", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Check if document was saved
        new_count = collection.count_documents({})
        print(f"   Documents added: {new_count - initial_count}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Test smart command processor (POST endpoint)
    print("\n3. Testing smart command processor...")
    try:
        data = {'command': 'hello from smart command'}
        response = requests.post(
            f"{base_url}/smart-command/", 
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Check if document was saved
        final_count = collection.count_documents({})
        print(f"   Total documents added: {final_count - initial_count}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Check recent documents
    print("\n4. Checking recent documents...")
    try:
        recent_docs = list(collection.find().sort('timestamp', -1).limit(5))
        for i, doc in enumerate(recent_docs, 1):
            timestamp = doc.get('timestamp', 'No timestamp')
            user_input = doc.get('user_input', 'No input')
            print(f"   {i}. {timestamp} - {user_input}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_web_interface_mongodb()