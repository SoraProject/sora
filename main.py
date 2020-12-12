# coding: UTF-8
import discord
from discord.ext import commands
import os
import pathlib
from utils import Dropbox as dropbox

TOKEN = os.environ['TOKEN']
command_prefix = ['!'] #Prefix

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.ready_check = False  # Variable to prevent duplicate on_ready events from being triggered
        super().__init__(*args, **kwargs)

    async def on_ready(self):

        if self.ready_check == False:

            print(f'import')
            if not self.loaded:
                import pathlib
                cur = pathlib.Path('.')
                for p in cur.glob('module/*.py'):
                    try:
                        print(f'module.{p.stem}', end="　")
                        self.load_extension(f'module.{p.stem}')
                        print(f'success')
                    except commands.errors.NoEntryPointError:
                        print(f'module.{p.stem}')
            else:
                self.loaded = True
            print('------')

            await dropbox().download_database()

            print('------')
            self.ready_check = True
        
        else:
            print('The start up process is already complete!')


intent: discord.Intents = discord.Intents.all()
bot = MyBot(command_prefix=command_prefix, intents=intent)

bot.run(TOKEN)
