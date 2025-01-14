from discord.ext import commands
from loguru import logger


class Client(commands.Cog):
    def __init__(self):
        super().__init__()

    @commands.command("sanitycheck")
    async def sanitycheck(self, ctx: commands.Context):
        logger.info(f'user "{ctx.author.name}" triggered sanitycheck')
        await ctx.reply("the bot is online!")
