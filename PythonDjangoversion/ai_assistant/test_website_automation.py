#!/usr/bin/env python
"""
Test script for website automation functionality
"""
import os
import sys
import django

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_assistant.settings')
django.setup()

from assistant.action import Action
from assistant.web_automation import open_whatsapp, open_youtube, open_instagram

def test_website_automation():
    print("🚀 Testing Website Automation Features")
    print("=" * 50)
    
    # Test 1: WhatsApp
    print("\n1. Testing WhatsApp automation...")
    try:
        success, message = open_whatsapp()
        print(f"   Status: {'✅ Success' if success else '❌ Failed'}")
        print(f"   Message: {message}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Instagram
    print("\n2. Testing Instagram automation...")
    try:
        success, message = open_instagram()
        print(f"   Status: {'✅ Success' if success else '❌ Failed'}")
        print(f"   Message: {message}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: YouTube
    print("\n3. Testing YouTube automation...")
    try:
        success, message = open_youtube()
        print(f"   Status: {'✅ Success' if success else '❌ Failed'}")
        print(f"   Message: {message}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Action function integration
    print("\n4. Testing Action function integration...")
    test_commands = [
        "open whatsapp",
        "open instagram", 
        "open youtube"
    ]
    
    for command in test_commands:
        try:
            response = Action(command)
            print(f"   Command: '{command}'")
            print(f"   Response: {response}")
            print()
        except Exception as e:
            print(f"   ❌ Error with '{command}': {e}")
    
    print("=" * 50)
    print("🎉 Website automation testing complete!")
    print("\n💡 To test the sidebar feature:")
    print("   1. Run: python manage.py runserver")
    print("   2. Open: http://127.0.0.1:8000")
    print("   3. Try commands: 'open whatsapp', 'open instagram', 'open youtube'")
    print("   4. Check the edge panel on the right side")

if __name__ == "__main__":
    test_website_automation()