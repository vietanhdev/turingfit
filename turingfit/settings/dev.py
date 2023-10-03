from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "1_zrwwz(3wk+je0e0*s552gdbb+m)ft9f#1&27tmw@f^b7jri1dfg"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "database.db",
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # project
]

ALLOWED_HOSTS = ["*"]
