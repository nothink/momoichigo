"""
ASGI config for momoichigo project.

sa: https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "momoichigo.settings")

application = get_asgi_application()
