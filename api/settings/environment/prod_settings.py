from datetime import timedelta

from decouple import Csv, config

from api.settings.components.drf_settings import REST_FRAMEWORK, SIMPLE_JWT

# ================
# DJANGO SETTINGS
# ================
DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# SMTP BACKEND https://docs.djangoproject.com/en/4.2/topics/email/#smtp-backend
EMAIL_HOST = config("EMAIL_HOST")

EMAIL_PORT = config("EMAIL_PORT")

EMAIL_HOST_USER = config("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

EMAIL_USE_TLS = True

# ADMIN SITE https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#adminsite-attributes
ADMIN_SITE_HEADER = config("ADMIN_SITE_HEADER")

ADMIN_SITE_TITLE = config("ADMIN_SITE_TITLE")

ADMIN_INDEX_TITLE = config("ADMIN_INDEX_TITLE")

ADMIN_URL = config("ADMIN_URL")


# ===============================
# DJANGO REST FRAMEWORK SETTINGS
# ===============================
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "anon": config("ANON_THROTTLE_RATE"),
    "user": config("USER_THROTTLE_RATE"),
}

SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(
    hours=config("ACCESS_TOKEN_LIFETIME", cast=int)
)

SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"] = timedelta(
    days=config("REFRESH_TOKEN_LIFETIME", cast=int)
)
