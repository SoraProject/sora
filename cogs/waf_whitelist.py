import dis
import aiosqlite3
import discord
from discord.ext import commands
from utils import WafGuild, CheckGuild, Database, Message as message, BotPermission


class Cog(commands.Cog):

    def __init__(self, bot):
        self.bot=bot
        self.waf_guild = WafGuild()
        self.check_guild = CheckGuild()
        self.database = Database()

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if self.check_guild.is_guild(member.guild, self.waf_guild) and self.database.has_database():
            member_datas: list = await self.database.fetch_database(self.waf_guild.whitelist_table)
            if not member.id in member_datas:
                await member.send(f"{member.mention}->あなたは#WAFのホワイトリストに追加されていないためキックされました。管理人に追加してほしい旨をお伝え下さい。")
                await member.kick(reason="ホワイトリストにいないため")

    @commands.command()
    async def add_whitelist(self, ctx: commands.Context, user: discord.User):
        waiting = await message.waiting(ctx)
        if (await BotPermission.is_admin(self.bot, ctx.author)):
            await self.database.add_data("waf_white_list", data=[user.id])
            await waiting.edit(content=f"{ctx.author.mention}->{user}をホワイトリストに追加しました！")
        

def setup(bot):
    bot.add_cog(Cog(bot))