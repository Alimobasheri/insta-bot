from flask_sqlalchemy import SQLAlchemy
from scraper import InstaBot

db = SQLAlchemy()

from server.app import create_app