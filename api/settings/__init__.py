from os import environ

from split_settings.tools import include, optional

ENV = environ.get("DJANGO_ENV") or "dev"

base_settings = [
    "components/base_settings.py",
    "components/database_settings.py",
    "components/drf_settings.py",

    f"environment/{ENV.lower()}_settings.py",

    optional("environment/local_settings.py")
]

include(*base_settings)
