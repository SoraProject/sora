import discord
from discord.ext import commands

class BotPermission:

    @staticmethod
    async def is_admin(bot :commands.Bot, ctx :commands.Context):
        """
        指定したユーザーがBot管理者か確認します。
        """
        try:
            if [i for i in (await (await bot.fetch_guild(787276328985952276)).fetch_member(ctx.author.id)).roles if i.id == 787276328985952276]:
                return True
            else:
                return False
        except:
            return False
