"""App configuration."""
from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY', "abc123abc123abc123abc123")
    WTF_CSRF_SECRET_KEY = environ.get('WTF_CSRF_SECRET_KEY', 'what09897what1234WHAT0987')

    # mongodb connection
    MONGO_DBNAME = 'what2do2day'
    MONGO_URI = 'mongodb+srv://' + environ.get("DB_USER") + ':' + environ.get("DB_PASS") +\
                '@mhavlicfirstcluster-pielp.mongodb.net/what2do2day?retryWrites=true&w=majority?'
    MONGO_SERVER_SELECTION_TIMEOUT_MS = '2000'
    MONGO_SOCKET_TIMEOUT_MS = '2000'
    MONGO_CONNECT_TIMEOUT_MS = '2000'
    GOOGLE_MAP_KEY = environ.get("GOOGLE_MAP_KEY")
