from discord.ext import commands
import discord
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
        try:
            user: discord.User = await ctx.bot.fetch_user(id)
            strikes = self.db.add_strikes(id)

            if strikes >= get_config()["MAX_STRIKES"]:
                print(user, type(user))
                await ctx.message.guild.ban(user)
                await ctx.reply(
                    f"the user **{user.display_name}** got banned for meeting the maximum amount of strikes\n"
                    + f"their strikes: {strikes}"
                )
            else:
                await ctx.reply(
                    f"the user **{user.display_name}** currently got {strikes} strikes"
                )

        except Exception as e:
            logger.error(f"error in strike: {e}")
            await ctx.reply(
                "cannot fetch the user's data, are you sure they are in this server?"
            )

    @commands.command("config")
    async def config(self, ctx: commands.Context):
        cfg = get_config()
        text = f"max strikes for a user: {cfg["MAX_STRIKES"]}\n"

        embed = discord.Embed(title="kittymod's config", description=text)
        await ctx.reply(embed=embed)
