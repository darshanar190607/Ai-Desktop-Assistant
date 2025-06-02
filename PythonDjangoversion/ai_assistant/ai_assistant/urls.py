from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('assistant.urls')),
    path('browser/', include('ai_assistant.web_ui.urls')),  #Future goals
]
