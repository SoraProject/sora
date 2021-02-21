import discord
from discord.ext import commands
from utils import my_channel
from typing import Union, Callable, List


class voice:

    @staticmethod
    def is_active(channel: discord.VoiceChannel, count_bots=True) -> bool:
        """
        通話に人がいるかどうかを確認します。
        """

        if count_bots:
            member_count: int = len(channel.members)

        else:
            member_count: int = len(
                [i for i in channel.members if i.bot is False])

        if channel is None or member_count > 0:
            return True

        else:
            return False

    @staticmethod
    def is_muted_text_channel(channel: discord.TextChannel) -> bool:
        """
        指定したチャンネルが聞き専チャンネルかどうか確認します。
        """
        topic_split: list = my_channel.get_topic(channel, split=True)
        if topic_split[0] == "これは自動生成されたテキストチャンネルです。":
            return True
        else:
            return False

    def is_voice_control_panel(self, message: discord.Message, bot: commands.Bot) -> bool:
        """
        指定したメッセージが自動生成されたボイスチャンネルのコントロールパネルか確認します。
        """
        try:
            if message.embeds[0].description == self.control_panel_description() and message.author == bot.user:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def is_generate_voice_channel(channel: discord.VoiceChannel) -> bool:
        """
        指定したチャンネルがボイスチャンネルを生成するチャンネルか確認します。
        """
        generate_channel_ids = [807784449067843584, 807784369166352384, 808647004410478592]
        if channel.id in generate_channel_ids:
            return True
        else:
            return False

    def is_auto_voice_channel(self, channel: discord.VoiceChannel) -> bool:
        """
        指定されたチャンネルが生成されたボイスチャンネルか確認します。
        """
        voice_category_ids = [807783200566411315, 808299132513943553, 808646855055376405]
        if channel.category.id in voice_category_ids and not self.is_generate_voice_channel(
                channel) and channel != channel.guild.afk_channel:
            return True
        else:
            return False

    @staticmethod
    def generate_auto_voice_topic(vc: discord.VoiceChannel, member: discord.Member) -> str:
        """
        自動生成されたチャンネルのトピックを生成します。
        """
        return f"これは自動生成されたテキストチャンネルです。\n{vc.id}\n{member.id}"

    async def clean_null_auto_voice_channels(self, category: discord.CategoryChannel) -> List[str]:
        """
        誰もいない自動生成されたボイスチャンネルを検知し、削除します。
        """
        id_list = []
        channel: discord.VoiceChannel
        for channel in category.channels:
            if type(channel) == discord.VoiceChannel:
                if not self.is_active(channel) and self.is_auto_voice_channel(channel):
                    id_list.append(str(channel.id))
                    await channel.delete(reason="誰もいないため")
        return id_list

    @staticmethod
    async def clean_null_auto_text_channels(category: discord.CategoryChannel,
                                            channels: Callable[[discord.CategoryChannel], list]):
        """
        使われていない自動生成されたテキストチャンネルを検知し、削除します。
        ※第二引数でclean_null_auto_voice_channelsを呼び出す想定で実装しています。
        """
        for channel in category.channels:
            if type(channel) == discord.TextChannel:
                topic = my_channel.get_topic(channel, split=True)
                if topic is None:
                    continue
                elif topic[1] in channels:
                    await channel.delete(reason="誰もいないため")

    @staticmethod
    async def get_auto_voice_owner(channel: discord.TextChannel) -> Union[discord.Member, None]:
        """
        自動生成されたチャンネルのオーナーのメンバーオブジェクトを返します。
        取得できなかった場合はNoneが返ります。
        """
        owner_id = my_channel.get_topic(channel, split=True)[2]
        try:
            return await channel.guild.fetch_member(int(owner_id))
        except:
            return None

    @staticmethod
    def is_hide(channel: discord.VoiceChannel) -> bool:
        guild: discord.Guild = channel.guild
        everyone_perms = dict(channel.overwrites_for(guild.default_role))

        if everyone_perms['view_channel']:
            return False

        return True

    @staticmethod
    def control_panel_description() -> str:
        """
        コントロールパネルのdescriptionを呼び出すショートカット関数です。
        """
        return "ここでは、該当するリアクションを押すことで様々な設定を行うことが出来ます。\n\n✏：チャンネル名の変更\n\n🔒：利用可能人数の制限"

    @staticmethod
    def get_linked_mute_channel(category: discord.CategoryChannel, vc: discord.VoiceChannel):
        for i in category.channels:
            topic = my_channel.get_topic(i, split=True)
            if topic[1] == vc.id:
                return i

