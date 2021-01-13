import discord
from discord.ext import commands
from pathlib import Path
from .validation import is_moderator, is_mod_commands_channel
import json


class MemberStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def m_stats(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        with open('./server_specific/channel_ids_test.json', 'r') as id_file:
            channel_id_dict = json.loads(id_file.read())
            guild_id = channel_id_dict['GUILD']
            guild = self.bot.get_guild(guild_id)

            true_member_count = 0
            member_online_count = 0

            for member in guild.members:
                if not member.bot:
                    true_member_count += 1
                    if member.status == discord.Status.online:
                        member_online_count += 1

            await ctx.send(f'Total members: {true_member_count}')
            await ctx.send(f'Online members: {member_online_count}')
