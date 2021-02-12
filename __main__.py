from instagram_scraper import InstagramScraper

import json

class InstaBot(InstagramScraper):
    def __init__(self, user, username, password):
        super().__init__(usernames=[user], login_user=username, login_pass=password)
    
    def save_captions(self):
        data_file = f'./datas/{self.usernames[0]}.json'
        
        try:
            with open(data_file) as f:
                user_json = json.load(f)
        except Exception as e:
            user_json = None

        if len(self.captions) > 0 and user_json is not None:
            user = json.loads(user_json)
            for caption in self.captions:
                user["captions"].append(caption)
            self.save_json(user, data_file)
        elif len(self.captions) > 0:
            user = {
                "captions": []
            }
            for caption in self.captions:
                user["captions"].append(caption)

''' Example
bot = InstaBot(user="jzarif_ir", username="amade_nabard", password="gogoshbash1380")
bot.maximum = 5 
bot.authenticate_with_login()
bot.scrape()
bot.save_cookies()
'''