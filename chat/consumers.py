import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from authorization.models import CustomUser
from channels.db import database_sync_to_async

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0
)


class ConnectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = f'chat_connected'
        self.user = self.scope['url_route']['kwargs']['user_id']
        print(self.user)

        self.user_obj = await database_sync_to_async(CustomUser.objects.get)(id=self.user)
        user_category=''
        try:
            print(self.user_obj.teacher.faculty)
            user_category='Teacher'
        except:
            user_category='Student'
            
        user_data = {
            'id':self.user, 'first_name':self.user_obj.first_name,
            'last_name': self.user_obj.last_name, 'username':self.user_obj.username,
            'email':self.user_obj.email, 'token':'Not Allowed',
            'user_category':user_category
        }
        
        redis_client.sadd('connected_users', json.dumps(user_data))
        redis_client.set(f'chat_user_{self.user}', self.channel_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.broadcast_connected_users()

    async def disconnect(self, close_code):
        redis_client.srem('connected_users', self.user)
        redis_client.delete(f'chat_user_{self.user}')

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.broadcast_connected_users()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user}: {message}'
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def broadcast_connected_users(self):
        connected_users = redis_client.smembers('connected_users')
        connected_users_list = list(map(lambda x: x.decode('utf-8'), connected_users))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'connected_users_message',
                'connected_users': connected_users_list
            }
        )

    async def connected_users_message(self, event):
        connected_users = event['connected_users']

        await self.send(text_data=json.dumps({
            'connected_users': connected_users
        }))



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        # redis_client.delete(f'chat_user_{self.user.id}')
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(self.room_group_name, {'type':'chat.message', 'message':f'{message}'})
        
    async def chat_message(self, event):
        message=event['message']
        await self.send(
            text_data=json.dumps({
                'message':message
            })
        )