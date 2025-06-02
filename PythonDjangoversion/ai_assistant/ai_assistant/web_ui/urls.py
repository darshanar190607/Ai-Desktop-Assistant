from django.urls import path
from . import views

urlpatterns = [
    path('', views.browser_ui, name='browser_ui'),
    path('navigate/', views.browser_navigate, name='browser_navigate'),
    path('task/', views.browser_task, name='browser_task'),
]