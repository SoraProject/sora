import discord


class WafGuild:

    def __init__(self):
        self.guild_id = 706513089541046303
        self.whitelist_table = "waf_white_list"

class SkyGuild:

    def __init__(self):
        self.guild_id = 705629561743736935

class CheckGuild:

    def is_guild(self, guild: discord.Guild, guild_obj: object):
        """
        指定したオブジェクトが指定したギルドのものか確認します。
        """
        if guild.id == guild_obj().guild_id:
            return True
        
        return False

