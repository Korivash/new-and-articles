from pymongo import MongoClient

class Database:
    def __init__(self, mongodb_uri: str):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client["cyber_news_bot"]
        self.channels = self.db["channels"]

    def save_article(self, article: dict):
        # Implement logic to prevent duplicate articles (e.g., check if URL exists)
        pass

    def remove_channel(self, channel_id: str):
        self.channels.delete_one({"channel_id": channel_id})

    def add_channel(self, channel_id: str, news_types: list):
        self.channels.insert_one({"channel_id": channel_id, "news_types": news_types})

    def get_channels_by_news_type(self, news_type: str):
        return list(self.channels.find({"news_types": news_type}))

