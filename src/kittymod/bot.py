from discord.ext import commands
from discord import Intents
from kittymod.config import get_config
import asyncio


class Bot:
    def __init__(self):
        INTENTS = Intents.all()

        self.bot = commands.Bot("%", intents=INTENTS)

    def add_cog(self, cog: commands.Cog):
        asyncio.run(self.bot.add_cog(cog))

    def run(self):
        self.bot.run(get_config()["TOKEN"])
