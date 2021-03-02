import discord
from discord.ext import commands
import asyncio


class Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.rank_dir = {
            ("Gミシック", "Gミシ"): 812658464039370792,
            ("ミシック", "ミシ"): 807577001057320970,
            ("レジェンド", "レジェ"): 807577433221496862,
            ("エピック", "エピ"): 807577433221496862,
            ("グランドマスター", "グラマス"): 807577449310453790,
            ("マスター", "マス"): 807577450128080936,
            ("エリート", "エリ"): 807577450905075722,
            ("ウォーリア"): 807577451957583882
        }
        self.introduction_channel_id = 807581526026879016

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.channel.id == self.introduction_channel_id:
            return

        base_content = message.content
        add_role_ids = []
        added_role_names = []
        add_roles = []

        def check_rank_sentence(base_content, rank_name):
            if rank_name in base_content:
                return True
            return False

        for rank_names, rank_role_id in self.rank_dir.items():

            for rank_name in rank_names:
                if check_rank_sentence(base_content, rank_name):
                    add_role_ids.append(rank_role_id)
                    break

        for role_id in add_role_ids:
            role = message.guild.get_role(role_id)
            add_roles.append(role)
            added_role_names.append(role.name)

        if not len(add_roles):
            await message.author.add_roles(*add_roles, reason="自己紹介での自動役職付与")
            sentence = f"自己紹介の文からランクを検知して以下のランク役職を付与しました。\n" \
                       f"{[f'`{i}` ' for i in added_role_names]}\n" \
                       f"⚠間違いがある場合はお手数ですが <#807586753300660264>で再設定を行ってください。"
            embed = discord.Embed(description=sentence, colour=0xff8566)
            embed.set_footer(text="このメッセージは15秒後に削除されます。")
            msg = await message.channel.send(f"{message.author.mention}->", embed=embed)
            await asyncio.sleep(15)
            await msg.delete()


def setup(bot):
    bot.add_cog(Cog(bot))
