from django.shortcuts import render
from django.http import JsonResponse
import pyttsx3
import json
from django.views.decorators.csrf import csrf_exempt
from .action import Action, alarms, unknown_questions
from .speech_to_text import speech_to_text
from .mongodb_utils import save_conversation, save_unknown_question, get_unknown_questions, mark_question_answered
from .web_automation import open_whatsapp, open_youtube, open_instagram, fill_google_form, google_shopping, parse_form_data, parse_shopping_query
import datetime
import re

def index(request):
    return render(request, 'assistant/index.html')

def process_input(request):
    user_input = request.GET.get('text')
    response = Action(user_input)
    
    # Save to MongoDB with error handling
    try:
        save_conversation(user_input, response)
    except Exception as e:
        print(f"Warning: Failed to save conversation to MongoDB: {e}")
        # Continue processing even if MongoDB save fails
    
    return JsonResponse({'response': response})

def speech_input(request):
    try:
        user_input = speech_to_text()
        response = Action(user_input)
        
        # Save to MongoDB with error handling
        try:
            save_conversation(user_input, response)
        except Exception as e:
            print(f"Warning: Failed to save conversation to MongoDB: {e}")
            # Continue processing even if MongoDB save fails
        
        return JsonResponse({'user_input': user_input, 'response': response})
    except Exception as e:
        return JsonResponse({'error': str(e)})

def check_mongodb(request):
    from .mongodb_utils import test_connection
    
    connection_status = test_connection()
    
    if connection_status:
        return JsonResponse({'status': 'success', 'message': 'MongoDB connection successful!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'MongoDB connection failed!'}, status=500)

def get_alarms(request):
    """Return all active alarms"""
    active_alarms = {}
    for alarm_id, alarm_data in alarms.items():
        if alarm_data["active"]:
            # Convert datetime to string for JSON serialization
            alarm_time_str = alarm_data["time"].strftime("%Y-%m-%d %H:%M:%S")
            active_alarms[alarm_id] = {
                "time": alarm_time_str,
                "active": alarm_data["active"]
            }
    
    return JsonResponse({'alarms': active_alarms})

@csrf_exempt
def set_alarm(request):
    """Set a new alarm"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            time_str = data.get('time')
            
            # Parse the time string
            formats = ["%H:%M", "%I:%M %p", "%I:%M%p"]
            parsed_time = None
            
            for fmt in formats:
                try:
                    parsed_time = datetime.datetime.strptime(time_str, fmt).time()
                    break
                except ValueError:
                    continue
            
            if not parsed_time:
                return JsonResponse({'success': False, 'message': 'Invalid time format'})
            
            # Get current date
            now = datetime.datetime.now()
            alarm_time = datetime.datetime.combine(now.date(), parsed_time)
            
            # If the time has already passed today, set for tomorrow
            if alarm_time < now:
                alarm_time = alarm_time + datetime.timedelta(days=1)
            
            # Store the alarm
            alarm_id = str(len(alarms) + 1)
            alarms[alarm_id] = {
                "time": alarm_time,
                "active": True
            }
            
            # Format time for display
            formatted_time = alarm_time.strftime("%I:%M %p")
            return JsonResponse({'success': True, 'message': f'Alarm set for {formatted_time}', 'alarm_id': alarm_id})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def delete_alarm(request, alarm_id):
    """Delete an alarm"""
    if alarm_id in alarms:
        del alarms[alarm_id]
        return JsonResponse({'success': True, 'message': 'Alarm deleted'})
    else:
        return JsonResponse({'success': False, 'message': 'Alarm not found'})

def get_unknown_questions_view(request):
    """Get all unknown questions"""
    try:
        # First try to get from MongoDB
        questions = get_unknown_questions()
        # Convert MongoDB ObjectId to string for JSON serialization
        questions_list = []
        for q in questions:
            q['_id'] = str(q['_id'])
            questions_list.append(q)
        
        # If MongoDB failed or returned empty, use the local file
        if not questions_list and unknown_questions:
            questions_list = unknown_questions
            
        return JsonResponse({'questions': questions_list})
    except Exception as e:
        # Fallback to local file if MongoDB fails
        return JsonResponse({'questions': unknown_questions, 'note': 'Using local file due to MongoDB error'})

@csrf_exempt
def answer_question(request, question_id):
    """Mark a question as answered with the provided answer"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            answer = data.get('answer')
            
            # Try to update in MongoDB
            try:
                from bson.objectid import ObjectId
                mark_question_answered(ObjectId(question_id), answer)
            except:
                # If MongoDB fails, update in local file
                for q in unknown_questions:
                    if q.get('id', '') == question_id:
                        q['answered'] = True
                        q['answer'] = answer
                        q['answered_at'] = datetime.datetime.now().isoformat()
                        
                # Save to local file
                import os
                file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'unknown_questions.json')
                with open(file_path, 'w') as f:
                    json.dump(unknown_questions, f, indent=4)
            
            return JsonResponse({'success': True, 'message': 'Question answered'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# New Web Automation Views

@csrf_exempt
def open_whatsapp_view(request):
    """Open WhatsApp desktop application"""
    try:
        success, message = open_whatsapp()
        return JsonResponse({'success': success, 'message': message})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
def open_youtube_view(request):
    """Open YouTube"""
    try:
        success, message = open_youtube()
        return JsonResponse({'success': success, 'message': message})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
def open_instagram_view(request):
    """Open Instagram"""
    try:
        success, message = open_instagram()
        return JsonResponse({'success': success, 'message': message})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
def fill_form_view(request):
    """Fill Google Form with provided data"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form_url = data.get('form_url')
            form_data = data.get('form_data', [])
            
            if not form_url:
                return JsonResponse({'success': False, 'message': 'Form URL is required'})
            
            if not form_data:
                return JsonResponse({'success': False, 'message': 'Form data is required'})
            
            success, message = fill_google_form(form_url, form_data)
            return JsonResponse({'success': success, 'message': message})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'POST method required'})

@csrf_exempt
def google_shopping_view(request):
    """Search and add products to cart on Google Shopping"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            search_query = data.get('search_query')
            max_price = data.get('max_price')
            
            if not search_query:
                return JsonResponse({'success': False, 'message': 'Search query is required'})
            
            success, message = google_shopping(search_query, max_price)
            return JsonResponse({'success': success, 'message': message})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'POST method required'})

@csrf_exempt
def smart_command_processor(request):
    """Process smart commands with enhanced parsing"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('command', '').lower()
            
            # WhatsApp command
            if "whatsapp" in user_input or "open whatsapp" in user_input:
                success, message = open_whatsapp()
                return JsonResponse({'success': success, 'message': message, 'action': 'whatsapp'})
            
            # YouTube command
            elif "youtube" in user_input:
                success, message = open_youtube()
                return JsonResponse({'success': success, 'message': message, 'action': 'youtube'})
            
            # Instagram command
            elif "instagram" in user_input:
                success, message = open_instagram()
                return JsonResponse({'success': success, 'message': message, 'action': 'instagram'})
            
            # Google Form filling command
            elif "fill form" in user_input:
                # Extract form URL and data from command
                url_pattern = r'https://[^\s]+'
                url_match = re.search(url_pattern, user_input)
                
                if url_match:
                    form_url = url_match.group()
                    form_data = parse_form_data(user_input)
                    
                    if form_data:
                        success, message = fill_google_form(form_url, form_data)
                        return JsonResponse({'success': success, 'message': message, 'action': 'fill_form'})
                    else:
                        return JsonResponse({
                            'success': False, 
                            'message': 'Please provide the data to fill. Example: "fill form https://forms.google.com/... with name John, email john@email.com"',
                            'action': 'fill_form'
                        })
                else:
                    return JsonResponse({
                        'success': False, 
                        'message': 'Please provide the Google Form URL. Example: "fill form https://forms.google.com/... with name John, email john@email.com"',
                        'action': 'fill_form'
                    })
            
            # Google Shopping command
            elif any(phrase in user_input for phrase in ["go to google and buy", "search and buy", "find and buy", "google shopping"]):
                search_query, max_price = parse_shopping_query(user_input)
                
                if search_query:
                    success, message = google_shopping(search_query, max_price)
                    return JsonResponse({'success': success, 'message': message, 'action': 'shopping'})
                else:
                    return JsonResponse({
                        'success': False, 
                        'message': 'Please specify what you want to buy. Example: "go to google and buy watch under 2000"',
                        'action': 'shopping'
                    })
            
            else:
                # Fallback to regular action processing
                response = Action(user_input)
                try:
                    save_conversation(user_input, response)
                except Exception as e:
                    print(f"Warning: Failed to save conversation to MongoDB: {e}")
                return JsonResponse({'success': True, 'message': response, 'action': 'general'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e), 'action': 'error'})
    
    return JsonResponse({'success': False, 'message': 'POST method required'})
