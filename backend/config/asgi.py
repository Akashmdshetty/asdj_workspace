import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings.production')
django.setup()

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import backend.collaboration.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            backend.collaboration.routing.websocket_urlpatterns
        )
    ),
})
