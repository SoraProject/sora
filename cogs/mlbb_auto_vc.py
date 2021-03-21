import discord
from discord.ext import commands
from utils import voice, my_channel, Message

reaction_list = ["✏", "🔒", "👀"]


# noinspection PyTypeChecker
class MlbbAutoVc(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.voice = voice()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):

        if member.voice is None:
            await self.voice.clean_null_auto_text_channels(
                before.channel.category,
                await self.voice.clean_null_auto_voice_channels(before.channel.category)
            )
            return

        elif not member.guild.id == self.bot.mlbb_guild_id:
            return

        elif not self.voice.is_generate_voice_channel(member.voice.channel):
            linked_channel = voice.get_linked_mute_channel(member.voice.channel.category, member.voice)
            await linked_channel.send(f"> {member}がVCに参加しました")
            return

        rank_vc_id = 807784369166352384
        match_vc_id = 807784449067843584
        talk_vc_id = 823151131903131648

        rank_vc: discord.VoiceChannel = self.bot.get_channel(rank_vc_id)
        match_vc: discord.VoiceChannel = self.bot.get_channel(match_vc_id)
        talk_vc: discord.VoiceChannel = self.bot.get_channel(talk_vc_id)
        author_channel: discord.VoiceChannel = member.voice.channel

        if author_channel == rank_vc or match_vc or talk_vc:

            global reaction_list
            if author_channel == match_vc or rank_vc:
                limit = 5

            else:
                limit = None

            if member.nick:
                ch_name = member.nick
            else:
                ch_name = member.display_name

            vc: discord.VoiceChannel = await author_channel.category.create_voice_channel(name=f"{ch_name}のVC",
                                                                                          limit=limit)
            await member.move_to(vc, reason="VCが生成されたため")
            muted_tc = await author_channel.category.create_text_channel(name=f"{ch_name}の聞き専チャンネル",
                                                                         topic=voice.generate_auto_voice_topic(
                                                                             member=member, vc=vc))
            embed = discord.Embed(title=f"{ch_name}のVCへようこそ！",
                                  description=voice.control_panel_description())
            msg = await muted_tc.send(embed=embed)

            for i in reaction_list:
                await msg.add_reaction(i)

        else:
            return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        if payload.member.bot:
            return

        channel: discord.TextChannel = self.bot.get_channel(payload.channel_id)
        guild: discord.Guild = self.bot.get_guild(payload.guild_id)
        rank_vc_id = 807784369166352384
        match_vc_id = 807784449067843584
        talk_vc_id = 808647004410478592

        if not self.voice.is_muted_text_channel(channel) or payload.member != await self.voice.get_auto_voice_owner(
                channel):
            return

        message: discord.Message = await channel.fetch_message(payload.message_id)

        if not self.voice.is_voice_control_panel(message, self.bot):
            return

        global reaction_list

        if not str(payload.emoji) in reaction_list:
            return

        await message.remove_reaction(payload.emoji, payload.member)

        if str(payload.emoji) == "✏":

            msg = await Message.question(
                bot=self.bot,
                main_object=message,
                member=payload.member,
                title=f"{payload.member.mention}->変更したい名前を入力してください。"
            )

            if msg is False:
                return

            result = msg['result']
            question = msg['question']

            if len(result.content) > 0:
                vc_id = int(my_channel.get_topic(channel, split=True)[1])
                if vc_id is None:
                    return await question.edit(content=f"{payload.member.mention}->不明なエラーが発生しました！")

                vc = self.bot.get_channel(vc_id)

                await channel.edit(name=result.content)
                await vc.edit(name=result.content)
                await channel.send(f"{payload.member.mention}->チャンネル名を`{result.content}`に変更しました！")

        elif str(payload.emoji) == "🔒":

            msg = await Message.question(
                bot=self.bot,
                main_object=message,
                member=payload.member,
                title=f"{payload.member.mention}->VCに入れる最大人数を指定してください。"
            )

            if msg is False:
                return

            result = msg['result']
            question = msg['question']

            try:
                num = int(result.content)
            except:
                return await question.edit(content=f"{payload.member.mention}->不正な値が渡されました！")

            if not num > 100:
                vc_id = int(my_channel.get_topic(channel, split=True)[1])
                if vc_id is None:
                    return await question.edit(content=f"{payload.member.mention}->不明なエラーが発生しました！")
                vc = self.bot.get_channel(vc_id)
                await vc.edit(user_limit=num)
                await channel.send(f"{payload.member.mention}->VCの参加可能人数を`{num}人`に変更しました！")
            else:
                return await question.edit(content=f"{payload.member.mention}->100人以上は指定できません！")

        elif str(payload.emoji) == "👀":

            if not self.voice.is_hide(payload.member.voice.channel):

                result = "非公開"

                vc: discord.VoiceChannel = self.bot.get_channel(my_channel.get_topic(channel, split=True)[1])

                for member in payload.member.voice.members:
                    await channel.set_permissions(
                        target=member,
                        view_channel=True,
                    )

                    await vc.set_permissions(
                        target=member,
                        view_channel=True,
                        connect=True
                    )

                await vc.set_permissions(
                    guild.default_role,
                    view_channel=False,
                    connect=False
                )

                await channel.set_permissions(
                    guild.default_role,
                    view_channel=False
                )

            else:

                result = "公開"

                vc: discord.VoiceChannel = self.bot.get_channel(my_channel.get_topic(channel, split=True)[1])

                await vc.set_permissions(
                    guild.default_role,
                    read_messages=True,
                    connect=True
                )

                await channel.set_permissions(
                    guild.default_role,
                    read_messages=True
                )

            await channel.send(
                content=f"{payload.member.mention}->このVCを`{result}`にしました！"
            )


def setup(bot):
    bot.add_cog(MlbbAutoVc(bot))
