import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# import mainh.routing
from django.urls import path
from mainh.consumers import IrisConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":URLRouter([
        path("ws/iris/", IrisConsumer.as_asgi()),
    ])
})
