from discord.ext import commands
from .validation import (is_moderator, is_mod_commands_channel,
                         asyncless_is_moderator,
                         asyncless_is_mod_commands_channel,
                         is_process_and_user_clear)
import json
import discord


class MuteMember(commands.Cog):
    """Class for commands related to muting Members"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def m_mute_member(self, ctx):
        """Mutes a Member"""
        # Validation
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        if not await is_process_and_user_clear(self.bot, 'm_mute_member', ctx):
            return
        
        # The check for messages in Seng conversation
        def check(m):
            return (
                asyncless_is_mod_commands_channel(m) and
                m.author.id == ctx.author.id and
                not m.content.startswith('$m')
            )

        # Ask for username and four digit discriminator
        await ctx.send('Please enter the username and the four digits of the '
                       'user to mute, wrapped in backticks (\`). For example, '
                       '`toxicPerson#1773`. Write \'cancel\' to cancel.')
        member_req_msg = await self.bot.wait_for('message', check=check)

        # Check if user wants to cancel
        if member_req_msg.content == 'cancel':
            await ctx.channel.send('Cancelling.')
            self.bot.processes['m_mute_member'] = None
            return
        
        # Realised that backtick code is unnecessary, but could be useful later
        # if moderators want to mute people for X duration.
        # Get leftmost backtick, and rightmost backtick
        l_index = member_req_msg.content.find('`')
        r_index = member_req_msg.content.rfind('`')
        if (l_index == -1) or (r_index == -1) or (l_index == r_index):
            await ctx.channel.send('Format looks incorrect. Please wrap the '
                                   'username and four digits in backticks '
                                   '(`).')
            await ctx.channel.send('Cancelling.')
            self.bot.processes['m_mute_member'] = None
            return
        
        # Get username and the discriminator
        username_four_digits = member_req_msg.content[l_index+1:r_index]
        username, four_digits = username_four_digits.split('#')

        # Get guild
        with open('./server_specific/channel_ids.json', 'r') as id_file:
            channel_id_dict = json.loads(id_file.read())
        guild_id = channel_id_dict['GUILD']
        guild = self.bot.get_guild(guild_id)

        # Get user
        user = discord.utils.get(guild.members, name=username, 
                                 discriminator=four_digits)

        # If the user does not seem to exist
        if user is None:
            await ctx.channel.send('Could not find that user. Ensure that you '
                                   'have entered their username and '
                                   'discriminator correctly.')
            await ctx.channel.send('Cancelling.')
            self.bot.processes['m_mute_member'] = None
            return
        
        # Assign mute to that user
        await user.add_roles(discord.utils.get(guild.roles, name='Muted'))
        await ctx.channel.send('Muted user.')
        self.bot.processes['m_mute_member'] = None

    @commands.command()
    async def m_unmute_member(self, ctx):
        """Unmutes a Member"""
        # Validation
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        if not await is_process_and_user_clear(self.bot, 'm_unmute_member',
                                               ctx):
            return
        
        # The check for messages in Seng conversation
        def check(m):
            return (
                asyncless_is_mod_commands_channel(m) and
                m.author.id == ctx.author.id and
                not m.content.startswith('$m')
            )

        # Ask for username and four digit discriminator
        await ctx.send('Please enter the username and the four digits of the '
                       'user to unmute, wrapped in backticks (\`). For '
                       'example, `toxicPerson#1773`. Write \'cancel\' to '
                       'cancel.')
        member_req_msg = await self.bot.wait_for('message', check=check)

        # Check if user wants to cancel
        if member_req_msg.content == 'cancel':
            await ctx.channel.send('Cancelling.')
            self.bot.processes['m_unmute_member'] = None
            return
        
        # Realised that backtick code is unnecessary, but could be useful later
        # if moderators want to mute people for X duration.
        # Get leftmost backtick, and rightmost backtick
        l_index = member_req_msg.content.find('`')
        r_index = member_req_msg.content.rfind('`')
        if (l_index == -1) or (r_index == -1) or (l_index == r_index):
            await ctx.channel.send('Format looks incorrect. Please wrap the '
                                   'username and four digits in backticks '
                                   '(`).')
            await ctx.channel.send('Cancelling.')
            self.bot.processes['m_unmute_member'] = None
            return
        
        # Get username and the discriminator
        username_four_digits = member_req_msg.content[l_index+1:r_index]
        username, four_digits = username_four_digits.split('#')

        # Get guild
        with open('./server_specific/channel_ids.json', 'r') as id_file:
            channel_id_dict = json.loads(id_file.read())
        guild_id = channel_id_dict['GUILD']
        guild = self.bot.get_guild(guild_id)

        # Get user
        user = discord.utils.get(guild.members, name=username, 
                                 discriminator=four_digits)

        # If the user does not seem to exist
        if user is None:
            await ctx.channel.send('Could not find that user. Ensure that you '
                                   'have entered their username and '
                                   'discriminator correctly.')
            await ctx.channel.send('Cancelling.')
            self.bot.processes['m_unmute_member'] = None
            return
        
        # Assign mute to that user
        await user.remove_roles(discord.utils.get(guild.roles, name='Muted'))
        await ctx.channel.send('Unmuted user.')
        self.bot.processes['m_unmute_member'] = None

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
                                          speak=False, stream=False)
        
        await ctx.send('Setup complete.')
