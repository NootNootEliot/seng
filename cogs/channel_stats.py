from discord.ext import commands
from pathlib import Path
from .validation import is_moderator, is_mod_commands_channel
import json

class ChannelStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cp_stats(self, ctx):

        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        with open('./server_specific/channel_ids.json', 'r') as id_file:
            channel_id_dict = json.loads(id_file.read())
            guild_id = channel_id_dict['GUILD']
            guild = self.bot.get_guild(guild_id)
            await ctx.send(f"Post stats in {guild}:")
            channel_count = 0
            for channel in guild.text_channels:
                count = 0
                channel_count += 1
                async for _ in channel.history(limit=None):
                    count += 1
                await ctx.send(f"{channel_count}. {channel.mention} : {count}")
