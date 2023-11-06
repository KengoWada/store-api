from decouple import config
from dj_database_url import parse as db_url

DATABASES = {"default": config("DATABASE_URL", cast=db_url)}
