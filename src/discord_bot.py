import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from typing import List
from db import Database
from scraper import Scraper
import os

class DiscordBot:
    def __init__(self, token: str, mongodb_uri: str):
        self.token = token
        self.db = Database(mongodb_uri)
        self.scraper = Scraper()
        self.intents = discord.Intents.default()
        self.intents.message_content = True  # Enable message content intent
        self.bot = commands.Bot(command_prefix='!', intents=self.intents)

        @self.bot.event
        async def on_ready():
            print(f'{self.bot.user} is ready')
            await self.bot.load_extension("commands") # Load commands
            try
            	synced = await self.bot.tree.sync()
            	print(f"Synced {len(synced)} command(s)")
            except Exception as e:
            	print(e)

    async def run(self):
        await self.bot.start(self.token)


class Commands(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command()
	async def ping(self, ctx: commands.Context):
		await ctx.send("Pong!")

	@app_commands.command(name="add_channel", description="Add a channel to receive news")
	@app_commands.describe(
		news_type = "The type of news to subscribe to (cybersecurity, world, etc.)"
	)
	async def add_channel(self, interaction: discord.Interaction, news_type: str):
		channel_id = str(interaction.channel_id)

		if await self.bot.db.is_channel_registered(channel_id):
			await interaction.response.send_message(f"This channel is already registered.", ephemeral=True)
			return

		await self.bot.db.add_channel(channel_id, [news_type])
		await interaction.response.send_message(f"Channel added to receive {news_type} news.", ephemeral=True)

	@app_commands.command(name="remove_channel", description="Remove this channel from receiving news")
	async def remove_channel(self, interaction: discord.Interaction):
		channel_id = str(interaction.channel_id)
		if not await self.bot.db.is_channel_registered(channel_id):
			await interaction.response.send_message(f"This channel is not registered.", ephemeral=True)
			return
		await self.bot.db.remove_channel(channel_id)
		await interaction.response.send_message(f"Channel removed from receiving news.", ephemeral=True)

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return
		# For testing purposes
		if message.content.startswith("$hello"):
			await message.channel.send("Hello!")


async def setup(bot: commands.Bot):
	bot.db = Database(os.getenv("MONGODB_URI"))
	await bot.add_cog(Commands(bot))

