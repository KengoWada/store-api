# ================
# DJANGO SETTINGS
# ================
DEBUG = True

ALLOWED_HOSTS = ["*"]


# ===============================
# DJANGO REST FRAMEWORK SETTINGS
# ===============================
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "anon": "1000/sec",
    "user": "1000/sec",
}

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
