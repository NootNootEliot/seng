from discord.ext import commands
from .validation import (is_moderator, is_mod_commands_channel,
                         asyncless_is_moderator,
                         asyncless_is_mod_commands_channel,
                         is_process_and_user_clear)
import json


class HallOfStars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.recording_status = False

    def get_guild(self):
        """Returns the guild object"""
        with open('./server_specific/channel_ids.json', 'r') as id_file:
            channel_id_dict = json.loads(id_file.read())
        guild_id = channel_id_dict['GUILD']
        return self.bot.get_guild(guild_id)

    # Record the message count for each Member in server history
    async def record_baseline(self):
        guild = self.get_guild()

        with open('./server_specific/mem_msg_count.json', 'w') as count_file:
            msg_dict = {}
            # Loop through every text channel in the guild
            for channel in guild.text_channels:
                # Loop through every message in the text channel
                async for msg in channel.history(limit=None):
                    # Check if that Member's already in the dictionary
                    if msg.author.id in msg_dict:
                        msg_dict[msg.author.id] = msg_dict[msg.author.id] + 1
                    else:
                        msg_dict[msg.author.id] = 1
            
            # Save the Member message file in JSON format
            count_file.write(json.dumps(msg_dict))

    # Start the message counting
    @commands.command()
    async def m_hos_start(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        if self.recording_status:
            await ctx.send('I\'m already recording!')
            return
        
        self.recording_status = True
        self.hos_update.start()
        await ctx.send('Started recording.')
    
    # Stop the message counting
    @commands.command()
    async def m_hos_stop(self):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        if not self.recording_status:
            await ctx.send('I\'m already not recording!')
            return
        
        self.recording_status = False
        self.hos_update.cancel()
        await ctx.send('Stopped recording.')
    
    # Outputs if messages are being recorded or not
    @commands.command()
    async def m_hos_status(self):
        pass
    
    # Force the Hall of Stars channel to update
    @commands.command()
    async def m_hos_force_update(self):
        pass
    
    # Update the Hall of Stars every 43200 seconds (12 hours)
    @tasks.loop(seconds=43200)
    async def hos_update(self):
        pass
