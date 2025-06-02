import pyttsx3
import os
import datetime
import webbrowser
import threading
import queue
import re
import random
import json
import os
from pathlib import Path
from .web_automation import (
    open_whatsapp, 
    open_youtube, 
    open_instagram,
    fill_google_form, 
    google_shopping,
    parse_form_data,
    parse_shopping_query,
)


engine = pyttsx3.init()


speech_queue = queue.Queue()


alarms = {}


unknown_questions = []


UNKNOWN_QUESTIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'unknown_questions.json')

if os.path.exists(UNKNOWN_QUESTIONS_FILE):
    try:
        with open(UNKNOWN_QUESTIONS_FILE, 'r') as f:
            unknown_questions = json.load(f)
    except:
        unknown_questions = []


motivational_quotes = [
    "Every day may not be good, but there's something good in every day.",
    "Believe you can and you're halfway there.",
    "The only way to do great work is to love what you do.",
    "Don't watch the clock; do what it does. Keep going.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "Your time is limited, don't waste it living someone else's life.",
    "The best way to predict the future is to create it.",
    "It does not matter how slowly you go as long as you do not stop.",
    "The only limit to our realization of tomorrow is our doubts of today."
]

entrepreneurial_tips = [
    "Focus on solving real problems that people face. The best businesses address genuine needs.",
    "Start small and validate your idea before investing too much time or money.",
    "Build a minimum viable product (MVP) to test your concept with real users.",
    "Listen to customer feedback and be willing to pivot if necessary.",
    "Network with other entrepreneurs and learn from their experiences.",
    "Don't be afraid of failure - it's often the best teacher in entrepreneurship.",
    "Focus on building a sustainable business model from the beginning.",
    "Invest time in understanding your target market and customer needs.",
    "Develop a clear value proposition that differentiates you from competitors.",
    "Be persistent and resilient - entrepreneurship is a marathon, not a sprint."
]

def tts_worker():
    while True:
        text = speech_queue.get()
        if text is None:  # Exit signal
            break
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()


threading.Thread(target=tts_worker, daemon=True).start()


def speak_async(text):
    speech_queue.put(text)

def detect_sad_emotion(text):
    sad_patterns = [
        r'\b(sad|depressed|unhappy|miserable|heartbroken|disappointed|upset|down|blue|gloomy)\b',
        r'\b(feeling low|feel terrible|feel awful|feel bad|feel down|feel sad)\b',
        r'\b(lost|hopeless|helpless|worthless|alone|lonely|isolated)\b',
        r'\b(crying|tears|sobbing|weeping)\b',
        r'\b(give up|can\'t go on|no point|what\'s the use)\b',
        r'\b(hate myself|hate my life|life is hard|life is tough)\b'
    ]
    
    for pattern in sad_patterns:
        if re.search(pattern, text.lower()):
            return True
    return False


def save_unknown_question(question):
    if question not in unknown_questions:
        unknown_questions.append({
            "question": question,
            "timestamp": datetime.datetime.now().isoformat(),
            "answered": False
        })
        
        # Save to file
        with open(UNKNOWN_QUESTIONS_FILE, 'w') as f:
            json.dump(unknown_questions, f, indent=4)

def set_alarm(time_str):
  
    try:
       
        formats = ["%H:%M", "%I:%M %p", "%I:%M%p"]
        parsed_time = None
        
        for fmt in formats:
            try:
                parsed_time = datetime.datetime.strptime(time_str, fmt).time()
                break
            except ValueError:
                continue
        
        if not parsed_time:
            return False, "I couldn't understand the time format. Please use HH:MM or HH:MM AM/PM."
        
        # Get current date
        now = datetime.datetime.now()
        alarm_time = datetime.datetime.combine(now.date(), parsed_time)
        
       
        if alarm_time < now:
            alarm_time = alarm_time + datetime.timedelta(days=1)
        
        
        alarm_id = str(len(alarms) + 1)
        alarms[alarm_id] = {
            "time": alarm_time,
            "active": True
        }
        
       
        formatted_time = alarm_time.strftime("%I:%M %p")
        return True, f"Alarm set for {formatted_time}"
    
    except Exception as e:
        return False, f"Error setting alarm: {str(e)}"


def Action(data):
    user_data = data.lower()
    
   
    if any(keyword in user_data for keyword in ["start business", "entrepreneur", "startup", "business idea", "business plan", "business model"]):
        response = f"Entrepreneur AI: {random.choice(entrepreneurial_tips)}"
    
   
    elif "set alarm" in user_data or "wake me up at" in user_data or "remind me at" in user_data:
        # Extract time using regex
        time_pattern = r'(\d{1,2}:\d{2}(?:\s*[ap]m)?|\d{1,2}\s*[ap]m)'
        time_match = re.search(time_pattern, user_data, re.IGNORECASE)
        
        if time_match:
            time_str = time_match.group(1)
            success, message = set_alarm(time_str)
            response = message
        else:
            response = "I couldn't find a time in your request. Please specify a time like '8:30 AM' or '14:30'."
    
    elif "your name" in user_data:
        response = "Hello, I am your Desktop AI assistant created by Darshan AR. How can I help you today?"

    elif "hello" in user_data or "hi" in user_data:
        response = "Hi, sir! How can I help you?"

    elif "good morning" in user_data:
        response = "Good morning sir!"

    elif "time now" in user_data:
        current_time = datetime.datetime.now()
        response = f"The time now is {current_time.hour} hour and {current_time.minute} minutes."

    elif "shutdown" in user_data:
        response = "Ok sir, shutting down."
        print("AI:",response)
        os.system("shutdown /s /t 1")

    elif "play music" in user_data:
        webbrowser.open("https://music.youtube.com/")
        response = "YouTube Music is now ready for you. Enjoy!"

    elif "youtube" in user_data:
        success, message = open_youtube()
        response = message

    elif "open google" in user_data:
        webbrowser.open("https://google.com/")
        response = "Google is now open."
    
    # WhatsApp functionality
    elif "whatsapp" in user_data or "open whatsapp" in user_data:
        success, message = open_whatsapp()
        response = message
    
    # Instagram functionality
    elif "instagram" in user_data or "open instagram" in user_data:
        success, message = open_instagram()
        response = message
    
    # Google Form filling functionality
    elif "fill form" in user_data and "google.com/forms" in user_data:
        # Extract form URL and data
        url_pattern = r'https://[^\s]+'
        url_match = re.search(url_pattern, user_data)
        
        if url_match:
            form_url = url_match.group()
            form_data = parse_form_data(user_data)
            
            if form_data:
                success, message = fill_google_form(form_url, form_data)
                response = message
            else:
                response = "Please provide the data to fill in the form. Example: 'fill form https://forms.google.com/... with name John, email john@email.com, phone 1234567890'"
        else:
            response = "Please provide the Google Form URL. Example: 'fill form https://forms.google.com/... with name John, email john@email.com'"
    
    elif "fill form" in user_data:
        response = "To fill a Google Form, please provide the form URL and data. Example: 'fill form https://forms.google.com/... with name John, email john@email.com, phone 1234567890'"
    
    # Google Shopping functionality
    elif any(phrase in user_data for phrase in ["go to google and buy", "search and buy", "find and buy", "google shopping"]):
        search_query, max_price = parse_shopping_query(user_data)
        
        if search_query:
            success, message = google_shopping(search_query, max_price)
            response = message
        else:
            response = "Please specify what you want to buy. Example: 'go to google and buy watch under 2000'"

    elif "how can i learn python" in user_data:
        response = "You can learn Python by practicing coding, using online resources, and working on projects. Would you like me to suggest some resources?"

    elif "how are you" in user_data:
        response = "I am fine, thank you! How can I assist you today?"

    elif "your age" in user_data:
        response = "I am a computer program, so I don't have an age like humans do. But I was created recently!"
        
    elif "your purpose" in user_data:
        response = "My purpose is to assist you with various tasks and provide information. How can I help you today?"

    elif "tell me a joke" in user_data:
        response = "Why did the computer go to the doctor? Because it had a virus!"

    elif "tell me a story" in user_data:
        response = (
            "Once upon a time, in a land far away, there lived a wise old owl who knew all the secrets of the forest. "
            "One day, a curious little mouse asked the owl for advice on how to be brave. "
            "The owl replied, 'Bravery is not the absence of fear, but the courage to face it.' "
            "And from that day on, the little mouse became known as the bravest creature in the forest."
        )

    elif "tell me a fact" in user_data:
        response = "Did you know that honey never spoils? Archaeologists found 3000-year-old honey in Egyptian tombs still edible!"

    elif "tell me a riddle" in user_data:
        response = "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I? (Answer: An echo)"

    elif "who is leela mam" in user_data:
        response = "Leela Mam is a teacher who teaches us Python programming. She is very knowledgeable and helpful."

    elif "who is darshan" in user_data:
        response = "Darshan is a student who created me as a project. He is very talented and hardworking."

    elif "your creator" in user_data:
        response = "My creator is Darshan AR, a talented programmer and student. He designed me to assist you."

    elif "favorite color" in user_data:
        response = "I don't have personal preferences, but I think blue is a nice color!"

    elif "favorite food" in user_data:
        response = "I don't eat food like humans do, but I think biryani is a popular favorite!"

    elif "favorite movie" in user_data:
        response = "I don't watch movies, but I hear that 'Inception' is a great one!"

    else:
        # Check for sad emotions and provide motivation
        if detect_sad_emotion(user_data):
            response = f"I noticed you might be feeling down. Remember: {random.choice(motivational_quotes)}"
        else:
            response = "Sorry, I'm not able to understand. Please explain clearly."
            # Save the unknown question
            save_unknown_question(user_data)

    # Speak response asynchronously
    speak_async(response)

    return response

# Optional main loop for command-line testing
if __name__ == "__main__":
    print("Desktop AI Assistant is running... (type 'exit' or 'quit' to stop)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            speak_async("Goodbye!")
            # Wait for all speech to finish before exiting
            speech_queue.join()
            break
        Action(user_input)
