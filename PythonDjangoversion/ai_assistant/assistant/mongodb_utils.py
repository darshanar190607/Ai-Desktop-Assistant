from pymongo import MongoClient
from django.conf import settings
import datetime
import logging

# Set up logging
logger = logging.getLogger(__name__)

def get_mongodb_collection(collection_name='demodatabase'):
    try:
        client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
        db = client[settings.MONGODB_DATABASE]
        collection = db[collection_name]
        return collection
    except Exception as e:
        logger.error(f"Failed to get MongoDB collection: {e}")
        raise

def save_conversation(user_input, assistant_response):
    try:
        collection = get_mongodb_collection()
        document = {
            'user_input': user_input,
            'assistant_response': assistant_response,
            'timestamp': datetime.datetime.now()
        }
        result = collection.insert_one(document)
        document['_id'] = result.inserted_id
        logger.info(f"Conversation saved to MongoDB with ID: {result.inserted_id}")
        return document
    except Exception as e:
        logger.error(f"Failed to save conversation to MongoDB: {e}")
        # Re-raise the exception so calling code knows it failed
        raise

def save_unknown_question(question):
    """Save questions that the AI couldn't answer to a separate collection"""
    collection = get_mongodb_collection('unknown_questions')
    document = {
        'question': question,
        'timestamp': datetime.datetime.now(),
        'answered': False,
        'answer': None
    }
    collection.insert_one(document)
    return document

def get_unknown_questions():
    """Retrieve all unknown questions"""
    collection = get_mongodb_collection('unknown_questions')
    return list(collection.find().sort('timestamp', -1))

def mark_question_answered(question_id, answer):
    """Mark a question as answered and store the answer"""
    collection = get_mongodb_collection('unknown_questions')
    collection.update_one(
        {'_id': question_id},
        {
            '$set': {
                'answered': True,
                'answer': answer,
                'answered_at': datetime.datetime.now()
            }
        }
    )

def test_connection():
    try:
        client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
        # The ismaster command is cheap and does not require auth
        client.admin.command('ismaster')
        print("MongoDB connection successful!")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False
