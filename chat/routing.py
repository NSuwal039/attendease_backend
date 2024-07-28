from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/connect/(?P<user_id>\w+)/$", consumers.ConnectConsumer.as_asgi()),
    re_path(r"ws/chat/room/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    
    
    
]