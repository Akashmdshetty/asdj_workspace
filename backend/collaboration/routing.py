from django.urls import re_path
from .consumers import document

websocket_urlpatterns = [
    re_path(r'ws/doc/(?P<room_name>\w+)/$', document.DocumentConsumer.as_asgi()),
]
