from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import ChatRoom

def chatPage(request, user):
    user_id = request.user.id
    return render(request, 'chat.html', {'room_name' : user, 'user_id': user_id})


def create_private_chat(request, participant):
    recipent = get_object_or_404(User, username=participant)

    room_name = f"private_room_chat_{min(request.user.id, recipent.id)}_{max(request.user.id, recipent.id)}"

    chat_room, created = ChatRoom.objects.get_or_create(
        name= room_name,
        type='private'
        )
    chat_room.paticipants.add(request.user, recipent)

    return chat_room