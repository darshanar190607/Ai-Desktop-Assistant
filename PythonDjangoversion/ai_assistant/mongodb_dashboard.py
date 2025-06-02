#!/usr/bin/env python
"""
MongoDB Dashboard - Monitor your MongoDB connection and data
Run this script to check the status of your MongoDB integration
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_assistant.settings')
django.setup()

from assistant.mongodb_utils import test_connection, get_mongodb_collection, save_conversation
from django.conf import settings

def print_header(title):
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def print_section(title):
    print(f"\n📊 {title}")
    print("-" * 40)

def mongodb_dashboard():
    print_header("MONGODB CONNECTION DASHBOARD")
    
    # 1. Connection Status
    print_section("Connection Status")
    if test_connection():
        print("✅ MongoDB Connection: SUCCESSFUL")
        print(f"📍 URI: {settings.MONGODB_URI}")
        print(f"🗄️  Database: {settings.MONGODB_DATABASE}")
    else:
        print("❌ MongoDB Connection: FAILED")
        return
    
    # 2. Database Statistics
    print_section("Database Statistics")
    try:
        collection = get_mongodb_collection()
        total_docs = collection.count_documents({})
        print(f"📄 Total Conversations: {total_docs}")
        
        # Count documents from today
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_docs = collection.count_documents({
            'timestamp': {'$gte': today_start}
        })
        print(f"📅 Today's Conversations: {today_docs}")
        
        # Count documents from last 7 days
        week_ago = datetime.now() - timedelta(days=7)
        week_docs = collection.count_documents({
            'timestamp': {'$gte': week_ago}
        })
        print(f"📈 Last 7 Days: {week_docs}")
        
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
    
    # 3. Recent Conversations
    print_section("Recent Conversations (Last 5)")
    try:
        collection = get_mongodb_collection()
        recent_docs = list(collection.find().sort('timestamp', -1).limit(5))
        
        if recent_docs:
            for i, doc in enumerate(recent_docs, 1):
                timestamp = doc.get('timestamp', 'Unknown time')
                user_input = doc.get('user_input', 'No input')[:50]
                assistant_response = doc.get('assistant_response', 'No response')[:50]
                
                print(f"\n{i}. 🕒 {timestamp}")
                print(f"   👤 User: {user_input}...")
                print(f"   🤖 Assistant: {assistant_response}...")
        else:
            print("No conversations found")
            
    except Exception as e:
        print(f"❌ Error retrieving conversations: {e}")
    
    # 4. Unknown Questions Collection
    print_section("Unknown Questions")
    try:
        unknown_collection = get_mongodb_collection('unknown_questions')
        unknown_count = unknown_collection.count_documents({})
        unanswered_count = unknown_collection.count_documents({'answered': False})
        
        print(f"❓ Total Unknown Questions: {unknown_count}")
        print(f"⏳ Unanswered Questions: {unanswered_count}")
        
        if unanswered_count > 0:
            print("\nRecent Unanswered Questions:")
            unanswered = list(unknown_collection.find({'answered': False}).sort('timestamp', -1).limit(3))
            for i, q in enumerate(unanswered, 1):
                question = q.get('question', 'No question')[:60]
                timestamp = q.get('timestamp', 'Unknown time')
                print(f"   {i}. {question}... ({timestamp})")
                
    except Exception as e:
        print(f"❌ Error checking unknown questions: {e}")
    
    # 5. Test Save Function
    print_section("Live Test")
    try:
        test_input = f"Dashboard test at {datetime.now().strftime('%H:%M:%S')}"
        test_response = "Dashboard test response - MongoDB is working!"
        
        result = save_conversation(test_input, test_response)
        print("✅ Live Save Test: SUCCESSFUL")
        print(f"📝 Document ID: {result.get('_id', 'Unknown')}")
        
        # Verify the save
        collection = get_mongodb_collection()
        new_count = collection.count_documents({})
        print(f"📊 Updated Total Documents: {new_count}")
        
    except Exception as e:
        print(f"❌ Live Save Test: FAILED - {e}")
    
    # 6. Service Status
    print_section("System Status")
    try:
        import subprocess
        result = subprocess.run(['sc', 'query', 'MongoDB'], capture_output=True, text=True, shell=True)
        if 'RUNNING' in result.stdout:
            print("✅ MongoDB Service: RUNNING")
        else:
            print("⚠️  MongoDB Service: NOT RUNNING")
    except:
        print("❓ Could not check MongoDB service status")
    
    print_header("DASHBOARD COMPLETE")
    print("🎉 Your MongoDB integration is working properly!")
    print("💡 If you see any issues above, please check:")
    print("   - MongoDB service is running")
    print("   - Connection URI is correct")
    print("   - Database permissions are set")

if __name__ == "__main__":
    mongodb_dashboard()