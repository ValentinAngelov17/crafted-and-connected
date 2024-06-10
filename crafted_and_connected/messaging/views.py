# messaging/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
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
            content=message_content,
            is_read=False  # Mark the new message as unread
        )

        return JsonResponse({
            'user_id': request.user.id,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'message': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def chat_room(request, user_id):
    current_user = request.user
    target_user = get_object_or_404(CustomUser, id=user_id)

    chat_room = ChatRoom.objects.filter(participants=current_user).filter(participants=target_user).first()
    if not chat_room:
        chat_room = ChatRoom.objects.create(name=f"user_{current_user.id}_to_{target_user.id}")
        chat_room.participants.add(current_user, target_user)

    # Mark all messages in this chat room as read for the current user
    chat_room.messages.filter(user=target_user, is_read=False).update(is_read=True)

    context = {
        'room': chat_room,
        'room_json': json.dumps({
            'id': chat_room.id,
            'name': chat_room.name,
        }),
        'title': f"{target_user.first_name} {target_user.last_name}"
    }
    return render(request, 'messaging/chat_room.html', context)


@login_required
def messages_view(request):
    user = request.user
    chat_rooms = ChatRoom.objects.filter(participants=user)

    chat_room_details = []
    for room in chat_rooms:
        other_participant = room.participants.exclude(id=user.id).first()
        if other_participant:
            unread_count = room.messages.filter(user=other_participant, is_read=False).count()
            chat_room_details.append({
                'room_id': room.id,
                'user_id': other_participant.id,
                'first_name': other_participant.first_name,
                'last_name': other_participant.last_name,
                'unread_count': unread_count,
            })

    return render(request, 'messaging/messages.html', {'chat_room_details': chat_room_details})


@login_required
def delete_chat_room(request, room_id):
    try:
        chat_room = ChatRoom.objects.get(id=room_id)
        if request.user in chat_room.participants.all():
            chat_room.delete()
        else:
            return HttpResponseForbidden("You are not authorized to delete this chat room.")
    except ChatRoom.DoesNotExist:
        return redirect('messages_view')

    return redirect('messages_view')
