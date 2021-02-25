from . import insta_scraper
import importlib
importlib.reload(insta_scraper)
import requests
import concurrent.futures as futures
import json

class InstaBot(insta_scraper.InstagramScraper):
    def __init__(self, users, username, password):
        super().__init__(usernames=users, login_user=username, login_pass=password)