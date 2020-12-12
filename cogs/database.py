import imp
import discord
from discord.ext import commands, tasks
from utils import Dropbox

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    @tasks.loop(minutes=5)
    async def upload(self):
        Dropbox().upload_database()


def setup(bot):
    bot.add_cog(Cog(bot))