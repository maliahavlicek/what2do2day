"""App configuration."""
from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY', "abc123abc123abc123abc123")

    # mongodb connection
    MONGO_DBNAME = 'what2do2day'
    MONGO_URI = 'mongodb+srv://' + environ.get("DB_USER") + ':' + environ.get("DB_PASS") +\
                '@mhavlicfirstcluster-pielp.mongodb.net/what2do2day?retryWrites=true&w=majority?'
    MONGO_SERVER_SELECTION_TIMEOUT_MS = '2000'
    MONGO_SOCKET_TIMEOUT_MS = '2000'
    MONGO_CONNECT_TIMEOUT_MS = '2000'


