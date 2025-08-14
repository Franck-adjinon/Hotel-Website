from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]


CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
] 


# Détermine le niveau de logs selon DEBUG
DEFAULT_LOG_LEVEL = "DEBUG" if DEBUG else "INFO"   


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
    }
}


# Gestion des fichiers static
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles") 


# Activer la compression et le caching
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" 


# Configuration du système de logging
from logging.handlers import RotatingFileHandler

LOGGING["root"]["level"] = "WARNING" 


# Activer le mode demo
DEMO_MODE = True


# ? Sécurité
# Cookies sécurisés
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True  # HTTPS activé
# Cookies protégés contre JS
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
# HSTS activé
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
# Sous-domaines inclus dans HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# Active la XSS filter du navigateur
SECURE_BROWSER_XSS_FILTER = True
# pour empêcher le MIME sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True
