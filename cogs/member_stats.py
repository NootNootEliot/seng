import discord
from discord.ext import tasks, commands
from pathlib import Path
from .validation import is_moderator, is_mod_commands_channel
import json
import os
from os import path
from datetime import datetime
from dateutil import tz


class MemberStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status = 0

    def cog_unload(self):
        self.m_stats.cancel()

    @commands.command()
    async def m_stats_start(self, ctx):
        self.m_stats.start(ctx)
        self.status = 1
        await ctx.send(f'statistics recording started')

    @commands.command()
    async def m_stats_stop(self, ctx):
        self.m_stats.cancel()
        self.status = 0
        await ctx.send(f'statistics recording stopped')

    @commands.command()
    async def m_stats_status(self, ctx):
        if self.status == 1:
            await ctx.send(f'statistics recording is running')
        else:
            await ctx.send(f'statistics recording NOT running')

    @commands.command()
    async def m_stats_read(self, ctx):
        if self.status == 1:
            await ctx.send(f'first stop statistics recording ($m_stats_stop)')
        else:
            if path.exists('./server_specific/member_stats.csv'):
                with open('./server_specific/member_stats.csv',
                          'r') as stats_file:
                    contents = stats_file.read()
                    await ctx.send('note: recorded timezone is PST (UTC -8)')
                    await ctx.send(f'{contents}')
                    stats_file.close()
            else:
                await ctx.send(f'file wiped')

    @commands.command()
    async def m_stats_clear(self, ctx):
        def check(m):
            return (
                not m.content.startswith('$m')
            )
        await ctx.send(f'wipe ALL statistics? y(yes) / n(no)')

        while True:
            yes_no_msg = await self.bot.wait_for('message',  check=check)
            if yes_no_msg.content not in ['Y',  'y',  'N',  'n']:
                await ctx.send('enter either \'Y\' or \'N\'.')
                continue
            if yes_no_msg.content in ['N',  'n']:
                break
            if yes_no_msg.content in ['Y',  'y']:
                await ctx.send(f'statistics file cleared')
                os.remove('./server_specific/member_stats.csv')
                break

    @tasks.loop(seconds=3600.0)
    async def m_stats(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        with open('./server_specific/channel_ids.json', 'r') as id_file:
            channel_id_dict = json.loads(id_file.read())
            guild_id = channel_id_dict['GUILD']
            guild = self.bot.get_guild(guild_id)

            true_member_count = 0
            member_online_count = 0

            for member in guild.members:
                if not member.bot:
                    true_member_count += 1
                    if member.status != discord.Status.offline:
                        member_online_count += 1

            # now = datetime.now()
            from_zone = tz.gettz('UTC')
            to_zone = tz.gettz('America/Los_Angeles')

            utc_now = datetime.utcnow()
            my_now = utc_now.replace(tzinfo=from_zone)
            now = my_now.astimezone(to_zone)

            tsMonth = now.strftime("%m")
            tsDay = now.strftime("%d")
            tsYear = now.strftime("%Y")
            tsHour = now.strftime("%H")
            tsMinute = now.strftime("%M")
            tsSecond = now.strftime("%S")

            with open('./server_specific/member_stats.csv',
                      'a+') as stats_file:
                stats_file.write(f'{tsYear}-{tsMonth}-{tsDay},'
                                 f'{tsHour}:{tsMinute}:{tsSecond},'
                                 f'{true_member_count},'
                                 f'{member_online_count}\r\n'
                                 )
                stats_file.close()
