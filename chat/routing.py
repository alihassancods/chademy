from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/private/(?P<username>\w+)/$',
            consumers.PrivateConsumer.as_asgi()),
     re_path(r'ws/chat/(?P<group_name>[0-9a-f-]+)/$', consumers.GroupConsumer.as_asgi()),
]
