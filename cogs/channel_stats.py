from discord.ext import commands
from pathlib import Path
from .validation import is_moderator, is_mod_commands_channel
import json


class ChannelStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def m_cp_stats(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        with open('./server_specific/channel_ids.json', 'r') as id_file:
            channel_id_dict = json.loads(id_file.read())
            guild_id = channel_id_dict['GUILD']
            guild = self.bot.get_guild(guild_id)
            await ctx.send(f"Posts in {guild}:")
            for channel_count, channel in enumerate(guild.text_channels):
                msg_count = len(await channel.history(limit=None).flatten())
                await ctx.send(
                    f'{channel_count + 1}. {channel.mention} : {msg_count}'
                )
