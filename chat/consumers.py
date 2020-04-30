import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Message
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.room_name = str(min(self.sender_id,self.receiver_id)) + '-' + str(max(self.sender_id,self.receiver_id));
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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        mess = Message()
        mess.text = message
        mess.sender = User.objects.get(id = self.sender_id)
        mess.receiver = User.objects.get(id = self.receiver_id)
        mess.save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.sender_id,
                'time' : str(mess.created),
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        time = event['time']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'time' : time
        }))