# coding: UTF-8
import discord
from discord.ext import commands
import os
import pathlib
from utils import Dropbox as dropbox

TOKEN = os.environ['TOKEN']
command_prefix = ['!']  # Prefix


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.ready_check = False  # Variable to prevent duplicate on_ready events from being triggered
        self.mlbb_guild_id = 807562875996209172
        super().__init__(*args, **kwargs)

    async def on_ready(self):

        if self.ready_check is False:

            print(f'import')
            import pathlib
            cur = pathlib.Path('.')
            for p in cur.glob('cogs/*.py'):
                try:
                    print(f'module.{p.stem}', end="　")
                    self.load_extension(f'cogs.{p.stem}')
                    print(f'success')
                except commands.errors.NoEntryPointError:
                    print(f'module.{p.stem}')
            print('------')

            dropbox().download_database()

            print('------')
            self.ready_check = True

        else:
            print('The start up process is already complete!')


intent: discord.Intents = discord.Intents.all()
bot = MyBot(command_prefix=command_prefix, intents=intent)

bot.run(TOKEN)
