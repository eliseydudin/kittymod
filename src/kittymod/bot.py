from discord.ext import commands
from discord import Intents
import toml
import asyncio


class Bot:
    def __init__(self):
        INTENTS = Intents.all()

        self.bot = commands.Bot("%", intents=INTENTS)
        self._load_config()

    def _load_config(self):
        result = toml.load("kittymod.toml")
        self.TOKEN = result["TOKEN"]

    def add_cog(self, cog: commands.Cog):
        asyncio.run(self.bot.add_cog(cog))

    def run(self):
        self.bot.run(self.TOKEN)
