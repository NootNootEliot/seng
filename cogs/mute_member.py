from discord.ext import commands
from .validation import is_moderator, is_mod_commands_channel
import json


class MuteMember(commands.Cog):
    """Class for commands related to muting Members"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mute_member():
        """Mutes a Member"""
        pass

    @commands.command()
    async def unmute_member():
        """Unmutes a Member"""
        pass

    @commands.command()
    async def view_muted_members():
        """Outputs a list of all Members who are muted"""
        pass

    @commands.command()
    async def mute_perm_setup(self, ctx):
        """Sets up the mute permission setting on every channel in the guild"""
        # Validation
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        # Get the guild
        with open('./server_specific/channel_ids.json', 'r') as id_file:
            channel_id_dict = json.loads(id_file.read())
        guild_id = channel_id_dict['GUILD']
        guild = self.bot.get_guild(guild_id)    

        for channel in guild.text_channels:
            print(channel)