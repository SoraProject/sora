import discord
from discord.ext import commands

class Message:

    @staticmethod
    async def waiting(ctx):
        await ctx.send(f"{ctx.author.mention}->処理中です...")