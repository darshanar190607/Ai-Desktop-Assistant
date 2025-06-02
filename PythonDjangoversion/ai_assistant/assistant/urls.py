from django.urls import path
from . import views
from .mongodb_utils import test_connection

# Test MongoDB connection on startup
test_connection()

urlpatterns = [
    path('', views.index, name='index'),
    path('process/', views.process_input, name='process_input'),
    path('speech/', views.speech_input, name='speech_input'),
    path('check-mongodb/', views.check_mongodb, name='check_mongodb'),
    
    # New endpoints for alarms
    path('alarms/', views.get_alarms, name='get_alarms'),
    path('alarms/set/', views.set_alarm, name='set_alarm'),
    path('alarms/delete/<str:alarm_id>/', views.delete_alarm, name='delete_alarm'),
    
    # New endpoints for unknown questions
    path('unknown-questions/', views.get_unknown_questions_view, name='get_unknown_questions'),
    path('unknown-questions/answer/<str:question_id>/', views.answer_question, name='answer_question'),
    
    # New endpoints for web automation
    path('whatsapp/', views.open_whatsapp_view, name='open_whatsapp'),
    path('youtube/', views.open_youtube_view, name='open_youtube'),
    path('instagram/', views.open_instagram_view, name='open_instagram'),
    path('fill-form/', views.fill_form_view, name='fill_form'),
    path('google-shopping/', views.google_shopping_view, name='google_shopping'),
    path('smart-command/', views.smart_command_processor, name='smart_command'),
]
