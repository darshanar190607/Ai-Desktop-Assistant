#!/usr/bin/env python
import os
import sys
import django

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_assistant.settings')
django.setup()

from assistant.mongodb_utils import test_connection, save_conversation, get_mongodb_collection

def test_mongodb_connection():
    print("Testing MongoDB Connection...")
    print("=" * 50)
    
    # Test 1: Basic connection test
    print("1. Testing basic connection...")
    if test_connection():
        print("✓ Basic connection successful!")
    else:
        print("✗ Basic connection failed!")
        return False
    
    # Test 2: Test saving a conversation
    print("\n2. Testing save conversation...")
    try:
        result = save_conversation("Test user input", "Test assistant response")
        print(f"✓ Conversation saved successfully! Document ID: {result.get('_id', 'Unknown')}")
    except Exception as e:
        print(f"✗ Failed to save conversation: {e}")
        return False
    
    # Test 3: Test getting collection
    print("\n3. Testing collection access...")
    try:
        collection = get_mongodb_collection()
        count = collection.count_documents({})
        print(f"✓ Collection accessed successfully! Document count: {count}")
    except Exception as e:
        print(f"✗ Failed to access collection: {e}")
        return False
    
    # Test 4: Test retrieving recent conversations
    print("\n4. Testing data retrieval...")
    try:
        collection = get_mongodb_collection()
        recent_docs = list(collection.find().sort('timestamp', -1).limit(5))
        print(f"✓ Retrieved {len(recent_docs)} recent documents")
        for i, doc in enumerate(recent_docs, 1):
            print(f"   {i}. User: {doc.get('user_input', 'N/A')[:50]}...")
    except Exception as e:
        print(f"✗ Failed to retrieve data: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All MongoDB tests passed successfully!")
    return True

if __name__ == "__main__":
    test_mongodb_connection()