from discord.ext import commands

async def setup(bot: commands.Bot):
	await bot.load_extension("src.discord_bot")