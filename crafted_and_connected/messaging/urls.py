# messaging/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.chat_room, name='chat_room'),
    path('api/send_message/', views.send_message, name='send_message'),
    path('messages/', views.messages_view, name='messages_view'),
    path('delete/<int:room_id>/', views.delete_chat_room, name='delete_chat_room'),
]
