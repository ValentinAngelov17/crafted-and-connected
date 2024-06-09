# messaging/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.chat_room, name='chat_room'),
    path('api/send_message/', views.send_message, name='send_message'),
]
