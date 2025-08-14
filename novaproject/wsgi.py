"""
WSGI config for novaproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
# Check
print("MEDIA_ROOT content:", os.listdir(settings.MEDIA_ROOT))
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "novaproject.settings.prod")

application = get_wsgi_application()

# Monter le dossier MEDIA sous /media/
if hasattr(settings, "MEDIA_ROOT") and settings.MEDIA_ROOT:
    prefix = settings.MEDIA_URL.lstrip("/")  # "media/"
    application.add_files(str(settings.MEDIA_ROOT), prefix=prefix)
