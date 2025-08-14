from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# import dans le cadre de la gestion des paramètres du package unfold
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)  # Crée automatiquement le dossier logs

# Détermine le niveau de logs selon DEBUG
DEFAULT_LOG_LEVEL = "DEBUG" if DEBUG else "INFO"


# Application definition

INSTALLED_APPS = [
    # Ajout des apps relatif à unfold
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    # Fin d'ajout des apps relatif à unfold
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # Whitenoise
    "django.contrib.staticfiles",
    "nova.apps.NovaConfig",  # nova
    "django_cleanup.apps.CleanupConfig",  #  Ajout de cette ligne pour inclure Django cleanup
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Whitenoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "novaproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "novaproject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ("en", _("English")),
    ("de", _("German")),
    ("fr", _("French")),
)


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
# le chemin du dossier Static
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "novaproject/static"),
]


# Gestion des fichiers média
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# log
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "django.log"),
            "maxBytes": 5 * 1024 * 1024,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
    },
}


# Todo: Configuration de unfold
UNFOLD = {
    "SHOW_LANGUAGES": True,  # Afficher l'option de modification des langue
    "SITE_TITLE": "Gestion Hôtel Nova",
    "SITE_HEADER": "NOVA",
    "SITE_ICON": {
        "light": lambda request: static("png/logo.png"),  # light mode
        "dark": lambda request: static("png/logo.png"),  # dark mode
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml+png",
            "href": lambda request: static("favicon/favicon-32.png"),
        },
    ],
    "ENVIRONMENT": "nova.utils.environment_callback",
    "SIDEBAR": {
        "show_search": True,  # Activer/Désactiver la barre de recherche
        "show_all_applications": False,  # Activer/Désactiver la liste déroulante des applications
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,  # Ligne de séparation en haut
                "collapsible": True,  # Activer/Desactiver Empêche cette section d'être repliable
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Réservation"),
                        "icon": "event",
                        "link": reverse_lazy("admin:nova_reservation_changelist"),
                    },
                    {
                        "title": _("Réservation Chambre"),
                        "icon": "meeting_room",
                        "link": reverse_lazy(
                            "admin:nova_reservation_chambre_changelist"
                        ),
                    },
                    {
                        "title": _("Articles"),
                        "icon": "article",
                        "link": reverse_lazy("admin:nova_article_changelist"),
                    },
                    {
                        "title": _("Témoignages"),
                        "icon": "3p",
                        "link": reverse_lazy("admin:nova_testimony_changelist"),
                    },
                    {
                        "title": _("Gallerie"),
                        "icon": "photo_library",
                        "link": reverse_lazy("admin:nova_photo_changelist"),
                    },
                    {
                        "title": _("Emails newsletter"),
                        "icon": "newspaper",
                        "link": reverse_lazy("admin:nova_newsletteremail_changelist"),
                    },
                    {
                        "title": _("Nos Contacts"),
                        "icon": "call",
                        "link": reverse_lazy("admin:nova_contactcompany_changelist"),
                    },
                    {
                        "title": _("Emails Clients"),
                        "icon": "mail",
                        "link": reverse_lazy("admin:nova_emailsend_changelist"),
                    },
                    {
                        "title": _("Nos liens sociaux"),
                        "icon": "share",
                        "link": reverse_lazy(
                            "admin:nova_liensocialecompany_changelist"
                        ),
                    },
                    {
                        "title": _("Nos Chambres"),
                        "icon": "bed",
                        "link": reverse_lazy("admin:nova_chambre_changelist"),
                    },
                    {
                        "title": _("Nos plats"),
                        "icon": "room_service",
                        "link": reverse_lazy("admin:nova_plat_changelist"),
                    },
                    {
                        "title": _("Agents service client"),
                        "icon": "support_agent",
                        "link": reverse_lazy("admin:nova_serviceclient_changelist"),
                    },
                    {
                        "title": _("Informations de l'Hôtel"),
                        "icon": "list_alt",
                        "link": reverse_lazy("admin:nova_hotelinfo_changelist"),
                    },
                ],
            },
            {
                "title": _("Users & Groups"),
                "separator": True,  # Ligne de séparation en haut
                "collapsible": True,  # Activer/Desactiver Empêche cette section d'être repliable
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            # Liste des models qui afficheront une navigation tabs
            "models": [
                {
                    "name": "nova.chambre",
                    "detail": True,
                },
                {
                    "name": "nova.reservation_chambre",
                    "detail": True,
                },
            ],
            # Liste des tabs
            "items": [
                {
                    "title": _("Chambre"),
                    "link": reverse_lazy("admin:nova_chambre_changelist"),
                },
                {
                    "title": _("Réservation"),
                    "link": reverse_lazy("admin:nova_reservation_chambre_changelist"),
                },
            ],
        },
    ],
}

# Todo: Paramètres de gestion des envois de mails via gmail
# Charger les variables d'environnement
load_dotenv()

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))  # Convertir en entier
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"  # Convertir en booléen
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
