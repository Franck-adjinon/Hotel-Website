from .base import * 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = [
    "9b9a-2c0f-f0f8-606-fd00-cda-2817-fec-f723.ngrok-free.app",
    "127.0.0.1",
]
CSRF_TRUSTED_ORIGINS = [
    "https://9b9a-2c0f-f0f8-606-fd00-cda-2817-fec-f723.ngrok-free.app",
] 

# Détermine le niveau de logs selon DEBUG
DEFAULT_LOG_LEVEL = "DEBUG" if DEBUG else "INFO"   

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("NAME"),
        "USER": os.getenv("USER"),
        "PASSWORD": os.getenv("PASSWORD"),
        "HOST": "localhost",
        "PORT": "5432",
    }
}


# Configuration du système de logging
from logging.handlers import RotatingFileHandler
LOGGING["root"]["level"] = "DEBUG" 