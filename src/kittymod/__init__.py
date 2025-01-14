from kittymod.bot import Bot
from kittymod.client import Client


def main() -> None:
    bot = Bot()
    bot.add_cog(Client())

    bot.run()
