"""
WSGI config for momoichigo project.

sa: https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "momoichigo.settings")

application = get_wsgi_application()
