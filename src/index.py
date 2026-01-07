import os
import asyncio
from dotenv import load_dotenv
from discord_bot import DiscordBot

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MONGODB_URI = os.getenv('MONGODB_URI')

async def main():
    bot = DiscordBot(token=DISCORD_TOKEN, mongodb_uri=MONGODB_URI)
    await bot.run()

if __name__ == '__main__':
    asyncio.run(main())
