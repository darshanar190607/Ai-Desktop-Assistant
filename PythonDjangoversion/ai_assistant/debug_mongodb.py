#!/usr/bin/env python
import os
import sys
import django

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_assistant.settings')
django.setup()

from assistant.mongodb_utils import save_conversation, get_mongodb_collection
from assistant.action import Action
import datetime

def debug_conversation_saving():
    print("Debugging MongoDB Conversation Saving...")
    print("=" * 60)
    
    # Test 1: Check current document count
    print("1. Checking current document count...")
    try:
        collection = get_mongodb_collection()
        initial_count = collection.count_documents({})
        print(f"   Current document count: {initial_count}")
    except Exception as e:
        print(f"   Error getting count: {e}")
        return
    
    # Test 2: Simulate a conversation like the views.py does
    print("\n2. Simulating conversation saving (like views.py)...")
    test_input = "hello there"
    try:
        # This is exactly what happens in views.py
        response = Action(test_input)
        print(f"   Action response: {response}")
        
        # Save to MongoDB (this is what views.py does)
        result = save_conversation(test_input, response)
        print(f"   MongoDB save result: {result}")
        
    except Exception as e:
        print(f"   Error during conversation simulation: {e}")
        return
    
    # Test 3: Check if document count increased
    print("\n3. Checking if document count increased...")
    try:
        new_count = collection.count_documents({})
        print(f"   New document count: {new_count}")
        print(f"   Documents added: {new_count - initial_count}")
    except Exception as e:
        print(f"   Error getting new count: {e}")
        return
    
    # Test 4: Check the most recent documents
    print("\n4. Checking most recent documents...")
    try:
        recent_docs = list(collection.find().sort('timestamp', -1).limit(3))
        for i, doc in enumerate(recent_docs, 1):
            timestamp = doc.get('timestamp', 'No timestamp')
            user_input = doc.get('user_input', 'No input')
            assistant_response = doc.get('assistant_response', 'No response')
            print(f"   {i}. Time: {timestamp}")
            print(f"      User: {user_input}")
            print(f"      Assistant: {assistant_response[:100]}...")
            print()
    except Exception as e:
        print(f"   Error retrieving recent documents: {e}")
    
    # Test 5: Test direct MongoDB save without Action
    print("\n5. Testing direct MongoDB save...")
    try:
        direct_result = save_conversation("Direct test input", "Direct test response")
        print(f"   Direct save result: {direct_result}")
        
        final_count = collection.count_documents({})
        print(f"   Final document count: {final_count}")
    except Exception as e:
        print(f"   Error in direct save: {e}")

if __name__ == "__main__":
    debug_conversation_saving()