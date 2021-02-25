from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from django.contrib.auth.models import User
from .services.chat_services import save_message_to_db_get_message_dict
from .models import Message, Chat


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)
        new_message_to_group = save_message_to_db_get_message_dict(data_json)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, new_message_to_group
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user = event['user']
        timestamp = event['timestamp']
        message_id = event['message_id']

        if str(self.scope['user']) != user:
            Message.objects.filter(pk=message_id).update(is_read=True)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'timestamp': timestamp,
        }))
