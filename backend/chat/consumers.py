import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import ChatRoom, Messages
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async


def convert_message_to_json(messages : Messages):
    return [{'message': message.content, 'sender': message.sender.id } for message in list(messages)]


class ChatConsummer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return
        
        try:
            self.room = await ChatRoom.objects.aget(name=self.room_name)
        except ChatRoom.DoesNotExist:
            self.room = None

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
            )
        
        await self.accept()

        if self.room:
            messages = await self.get_message_history(self.room_name)

            await self.send(text_data=json.dumps({
                'type': 'chat_history',
                'message': messages,
                'username': 'user',
                'timestamp': '10:30'
            }))
            
        

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = int(data['id'])

        sender = await User.objects.aget(pk=sender_id)

        room = await ChatRoom.objects.aget(name=self.room_name)
        chat_message = await Messages.objects.acreate(
            chat_room = room,
            sender=sender,
            content=message
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': str(sender),
                'timestamp': str(chat_message.timestamp)
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))

    async def chat_history(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))

    @sync_to_async
    def add_participant_to_chatroom(self, user, room):
        if user not in room.paticipants.all():
            room.paticipants.add(user)

    @sync_to_async
    def get_message_history(self, room_name):
        try:
            chat_room = ChatRoom.objects.get(name=room_name)
        except ChatRoom.DoesNotExist:
            return []
        messages = Messages.objects.filter(chat_room=chat_room)

        print(convert_message_to_json(messages))
        return convert_message_to_json(messages) if messages else []
    


