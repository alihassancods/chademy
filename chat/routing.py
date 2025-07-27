from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/private/(?P<username>\w+)/$',
            consumers.PrivateConsumer.as_asgi()),
    re_path(r'ws/chat/group/(?P<group_name>\w+)/$',
            consumers.GroupConsumer.as_asgi()),
]
