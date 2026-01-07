import pymongo
from typing import List, Dict

class Database:
    def __init__(self, mongodb_uri: str):
        self.client = pymongo.MongoClient(mongodb_uri)
        self.db = self.client["cyber_news"]  # Database name
        self.channels = self.db["channels"]  # Collection for channels
        self.articles = self.db["articles"] # Collection for articles (deduplication)

    async def save_article(self, article: Dict) -> None:
        # Prevents duplicate articles based on URL
        if self.articles.find_one({'url': article['url']}):
            return  # Article already exists
        self.articles.insert_one(article)

    async def remove_channel(self, channel_id: str) -> None:
        self.channels.delete_one({"channel_id": channel_id})

    async def add_channel(self, channel_id: str, news_types: List[str]) -> None:
        self.channels.insert_one({"channel_id": channel_id, "news_types": news_types})

    async def get_channels_by_news_type(self, news_type: str) -> List[Dict]:
        return list(self.channels.find({"news_types": news_type}))

    async def is_channel_registered(self, channel_id: str) -> bool:
        return self.channels.find_one({"channel_id": channel_id}) is not None

    async def get_all_channels(self) -> List[Dict]:
        return list(self.channels.find({}))


# Example usage (not for execution):
# db = Database(mongodb_uri="your_mongodb_uri")
# asyncio.run(db.add_channel("12345", ["cybersecurity", "world"]))
# channels = asyncio.run(db.get_channels_by_news_type("cybersecurity"))
# print(channels)
