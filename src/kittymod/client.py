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
        if not self.is_mod(ctx.author.id):
            return

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
        if not self.is_mod(ctx.author.id):
            return

        cfg = get_config()
        log_channel = ctx.guild.get_channel(cfg["LOG_CHANNEL"])
        text = (
            f"max strikes for a user: **{cfg["MAX_STRIKES"]}**\n"
            + f"logging channel: **{log_channel.name}**\n"
        )

        embed = discord.Embed(title="kittymod's config", description=text)
        await ctx.reply(embed=embed)

    @commands.command("ban")
    async def ban(self, ctx: commands.Context, id: int):
        if not self.is_mod(ctx.author.id):
            return

        user: discord.User = await ctx.bot.fetch_user(id)
        ctx.message.guild.ban(user)
        await ctx.reply(f"succesfully banned the user **{user.display_name}**")

    @commands.command("khelp")
    async def khelp(self, ctx: commands.Context):
        if not self.is_mod(ctx.author.id):
            return

        text = """
`%sanitycheck` - check if the bot works and everything's okay
`%config` - get the kittymod's config
`%strike <id>` - increment a user's strike count, upon reaching the max amount of strikes they get banned
`%khelp` - see this message
`%ban <id>` - ban a user by this id
"""
        embed = discord.Embed(title="help", description=text)
        await ctx.reply(embed=embed)

    def is_mod(self, id: int) -> bool:
        return list(get_config()["MODERATORS"]).count(id) != 0
