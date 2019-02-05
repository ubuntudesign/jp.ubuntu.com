"""
Django settings for canonical project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY", "no_secret")
DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"

# See https://docs.djangoproject.com/en/dev/ref/contrib/
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "canonicalwebteam",
    "django.contrib.staticfiles",
]

ALLOWED_HOSTS = ["*"]

MIDDLEWARE_CLASSES = []

ROOT_URLCONF = "webapp.urls"
WSGI_APPLICATION = "webapp.wsgi.application"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_L10N = True
USE_TZ = True
STATIC_ROOT = "static"
STATIC_URL = "/static/"
STATICFILES_FINDERS = ["django_static_root_finder.StaticRootFinder"]
ASSET_SERVER_URL = (
    "https://res.cloudinary.com/"
    "canonical/image/fetch/q_auto,f_auto/"
    "https://assets.ubuntu.com/v1/"
)

# See http://tinyurl.com/django-context-processors
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "builtins": [
                "canonicalwebteam.get_feeds.templatetags",
                "webapp.templatetags.utils",
            ],
            "context_processors": [
                "django_asset_server_url.asset_server_url",
                "django.template.context_processors.request",
            ],
        },
    }
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "error_file": {
            "level": "WARNING",
            "filename": os.path.join(BASE_DIR, "django-error.log"),
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1 * 1024 * 1024,
            "backupCount": 2,
        }
    },
    "loggers": {
        "django": {
            "handlers": ["error_file"],
            "level": "WARNING",
            "propagate": True,
        }
    },
}
