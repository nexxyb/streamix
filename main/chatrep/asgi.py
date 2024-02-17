import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatrep.settings')
django.setup()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import sample.routing

websocket_urlpatterns = [
    # *containers.routing.websocket_urlpatterns,
    *sample.routing.websocket_urlpatterns,
]

application = ProtocolTypeRouter({
  'https': get_asgi_application(),
  'websocket': AuthMiddlewareStack(  # new
        URLRouter(websocket_urlpatterns)
    ),
      # new
})