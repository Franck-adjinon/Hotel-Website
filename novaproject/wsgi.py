import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# le settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "novaproject.settings.prod")

# 
application = get_wsgi_application()

# importer settings
from django.conf import settings
import os as pyos  

# WhiteNoise pour les statics
application = WhiteNoise(application, root=str(settings.STATIC_ROOT))

# Monter le dossier MEDIA sous /media/
if hasattr(settings, "MEDIA_ROOT") and settings.MEDIA_ROOT:
    prefix = settings.MEDIA_URL.lstrip("/")  # "media/"
    application.add_files(str(settings.MEDIA_ROOT), prefix=prefix)
