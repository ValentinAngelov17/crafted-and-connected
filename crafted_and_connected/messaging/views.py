# messaging/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from crafted_and_connected.authentication.models import CustomUser
from django.db.models import Q
import json


@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        room_id = data.get('room_id')
        message_content = data.get('message')

        room = get_object_or_404(ChatRoom, id=room_id)
        message = Message.objects.create(
            room=room,
            user=request.user,
            content=message_content
        )

        return JsonResponse({
            'user_id': request.user.id,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'message': message.content,

            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # Optionally include timestamp
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def chat_room(request, user_id):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')

    current_user = request.user
    target_user = get_object_or_404(CustomUser, id=user_id)

    existing_room = ChatRoom.objects.filter(
        participants=current_user
    ).filter(participants=target_user).first()

    if not existing_room:
        room_name = f"user_{current_user.id}_to_{target_user.id}"
        existing_room = ChatRoom.objects.create(name=room_name)
        existing_room.participants.add(current_user, target_user)

    if first_name and last_name:
        title = f"{first_name} {last_name}"
    else:
        title = "Chat Room"

    context = {
        'room': existing_room,
        'room_json': json.dumps({
            'id': existing_room.id,
            'name': existing_room.name,
        }),
        'title': title
    }

    return render(request, 'messaging/chat_room.html', context)
