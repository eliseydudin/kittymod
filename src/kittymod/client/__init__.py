from discord.ext import commands
from loguru import logger
from kittymod.database import Database
from kittymod.config import get_config


class Client(commands.Cog):
    def __init__(self):
        super().__init__()
        self.db = Database()

    @commands.command("sanitycheck")
    async def sanitycheck(self, ctx: commands.Context):
        logger.info(f'user "{ctx.author.name}" triggered sanitycheck')
        await ctx.reply("the bot is online!")

    @commands.command("strike")
    async def strike(self, ctx: commands.Context, id: int):
        strikes = self.db.add_strikes(id)
        await ctx.reply(f"the user **{id}** currently got {strikes} strikes")

        if strikes >= get_config()["MAX_STRIKES"]:
            user = await ctx.bot.fetch_user(id)
            print(user, type(user))
            await ctx.message.guild.ban(user)
            await ctx.reply(
                f"the user **{id}** got banned for meeting the maximum amount of strikes"
            )
