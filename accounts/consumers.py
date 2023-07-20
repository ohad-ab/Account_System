import json
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import Chat_Users
from asgiref.sync import async_to_sync, sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name  = f"chat_{self.room_name}"
        user = self.scope['user']
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.connect_user(user, self.room_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'enter_message',
                'username': user.username,
            }
        )

    async def disconnect(self, close_code):
        user = self.scope['user']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'exit_message',
                'username': user.username,
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.disconnect_user(user, self.room_name)

    @sync_to_async
    def connect_user(self, user, room_name):
        chat_room = Chat_Users.objects.get(name=room_name)
        if not chat_room.users.contains(user):
            chat_room.users.add(user)

    @sync_to_async
    def disconnect_user(self, user, room_name):
        chat_users = Chat_Users.objects.get(name=room_name)
        chat_users.users.remove(user)
        if chat_users.users.count == 0:
            chat_users.delete()
        


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'username': username,
        }))

    async def enter_message(self, event):
        await self.send(text_data=json.dumps(
            {
                'type':'enter',
                'username': event['username']
            }
        ))

    async def exit_message(self, event):
        await self.send(text_data=json.dumps(
            {
                'type':'exit',
                'username': event['username']
            }
        ))