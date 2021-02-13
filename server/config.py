"""Flask configuration variables."""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    """Set Flask configuration from .env file."""
    # General Config
    SECRET_KEY = "dev"

    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///instabot.db"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False