import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ChitChat(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user_id = self.scope["session"]["_auth_user_id"]
        self.group_name = f"{user_id}"
        await self.channel_layer.group.add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'receive group message',
                'message': message,
            }
        )
    async def receive_group_message(self, event):
        message =  event['message']
        await self.send(
            text_data=json.dumps({
                "message":message
            })
        )