"""App configuration."""
from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = environ.get('WTF_CSRF_SECRET_KEY')

    # mongodb connection
    MONGO_URI = environ.get('MONGO_URI_WHAT2DO2DAY')
    MONGO_SERVER_SELECTION_TIMEOUT_MS = '2000'
    MONGO_SOCKET_TIMEOUT_MS = '2000'
    MONGO_CONNECT_TIMEOUT_MS = '2000'

    # google
    GOOGLE_MAP_KEY = environ.get("GOOGLE_MAP_KEY")
