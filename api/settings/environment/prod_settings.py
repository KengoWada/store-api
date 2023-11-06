from datetime import timedelta

from decouple import Csv, config

# ================
# DJANGO SETTINGS
# ================
DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


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
