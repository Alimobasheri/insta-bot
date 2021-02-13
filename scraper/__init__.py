from instagram_scraper import InstagramScraper

import json

class InstaBot(InstagramScraper):
    def __init__(self, users, username, password):
        super().__init__(usernames=users, login_user=username, login_pass=password)
    
    def save_captions(self):
        return self.captions

''' Example
bot = InstaBot(user="jzarif_ir", username="amade_nabard", password="gogoshbash1380")
bot.maximum = 5 
bot.authenticate_with_login()
bot.scrape()
bot.save_cookies()
'''