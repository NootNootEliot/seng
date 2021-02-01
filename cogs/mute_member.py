from discord.ext import commands
from .validation import is_moderator, is_mod_commands_channel
import json
import discord


class MuteMember(commands.Cog):
    """Class for commands related to muting Members"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def m_mute_member(self, ctx):
        """Mutes a Member"""
        pass

    @commands.command()
    async def m_unmute_member(self, ctx):
        """Unmutes a Member"""
        pass

    @commands.command()
    async def m_view_muted_members(self, ctx):
        """Outputs a list of all Members who are muted"""
        pass

    @commands.command()
    async def m_mute_perm_setup(self, ctx):
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

        # Get the 'Muted' role
        muted_role = discord.utils.get(guild.roles, name='Muted')

        # Loop through every text channel and set permissions for Muted role
        for channel in guild.text_channels:
            await channel.set_permissions(muted_role, send_messages=False,
                                          add_reactions=False)
        
        # Loop through every voice channel and set permissions for Muted role
        for channel in guild.voice_channels:
            await channel.set_permissions(muted_role, connect=False,
                                          speak=False, video=False)
        
        await ctx.send('Setup complete.')
