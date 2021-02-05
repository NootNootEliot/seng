from discord.ext import commands
from .validation import (is_moderator, is_mod_commands_channel,
                         asyncless_is_moderator,
                         asyncless_is_mod_commands_channel,
                         is_process_and_user_clear)
import json


class HallOfStars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_recording = False
        self.msg_dict = {}

    def get_guild(self):
        """Returns the guild object"""
        with open('./server_specific/channel_ids.json', 'r') as id_file:
            channel_id_dict = json.loads(id_file.read())
        guild_id = channel_id_dict['GUILD']
        return self.bot.get_guild(guild_id)

    # Record the message count for each Member in server history
    async def record_baseline(self):
        guild = self.get_guild()

        # Loop through every text channel in the guild
        for channel in guild.text_channels:
            # Loop through every message in the text channel
            async for msg in channel.history(limit=None):
                # Check if that Member's already in the dictionary
                if msg.author.id in self.msg_dict:
                    self.msg_dict[msg.author.id] += 1
                else:
                    self.msg_dict[msg.author.id] = 1
    
    # Start recording and saving
    async def start_rec_sav(self, ctx):
        self.is_recording = True
        self.hos_update.start()
        self.save_msg_dict.start()
        await ctx.send('Started recording and saving.')

    # Start the message counting - loads in existing count file
    @commands.command()
    async def m_hos_start(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        if self.is_recording:
            await ctx.send('I\'m already recording!')
            return
        
        # Reset the msg_dict to be empty
        self.msg_dict = {}

        # Check if count file exists. If it does, start from those values
        if os.path.exists('./server_specific/count_file.json'):
            with open('./server_specific/count_file.json', 'r') as count_file:
                self.msg_dict = json.loads(count_file.read())

        start_rec_save(ctx)
    
    # Generates completely new (and potentially more accurate data) but takes
    # longer
    @commands.command()
    async def m_hos_fresh_start(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        if self.is_recording:
            await ctx.send('I\'m already recording!')
            return
        
        # Reset the msg dictionary to nothing
        self.msg_dict = {}

        # Record all data from the start of the Discord server afresh
        await ctx.send('Re-building data.')
        self.record_baseline()

        start_rec_save(ctx)
    
    # Stop the message counting
    @commands.command()
    async def m_hos_stop(self):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        if not self.is_recording:
            await ctx.send('I\'m already not recording/saving!')
            return
        
        self.is_recording = False
        # Save the dictionary so as to not lose stats hen starting up again
        self.save_msg_dict()
        self.hos_update.cancel()
        self.save_msg_dict.close()
        await ctx.send('Stopped recording and saving.')
    
    # Outputs if messages are being recorded or not
    @commands.command()
    async def m_hos_status(self):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        
        if self.is_recording:
            await ctx.send('I am recording and saving!')
        else:
            await ctx.send('I am not recording/saving!')
    
    # Listen to messages, and adds them to the file
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id in self.msg_dict:
            self.msg_dict[msg.author.id] += 1
        else:
            self.msg_dict[msg.author.id] = 1

    # Force the Hall of Stars channel to update
    @commands.command()
    async def m_hos_force_update(self):
        pass
    
    # Update the Hall of Stars every 43200 seconds (12 hours)
    @tasks.loop(seconds=43200)
    async def hos_update(self):
        pass
    
    # Save the data to a text f ile
    @tasks.loop(seconds=3600)
    async def save_msg_dict(self):
        # Every hour, save the msg dictionary to the count file
        with open('./server_specific/count_file.json', 'w') as count_file:
            count_file.write(json.dumps(self.msg_dict))
