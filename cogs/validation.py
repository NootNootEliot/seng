import json
from discord.ext import commands
from pathlib import Path


async def is_moderator(ctx):
    with open('server_specific/moderators.txt', 'r') as moderator_file:
        moderator_ids = moderator_file.read().splitlines()

    if str(ctx.author.id) not in moderator_ids:
        await ctx.send(
            '<@{}> - You do not have permission to use that command.'
            ''.format(ctx.author.id)
        )
        return False
    return True


async def is_mod_commands_channel(ctx):
    with open('server_specific/channel_ids.json', 'r') as id_file:
        mod_channel_id = json.loads(id_file.read())["MOD_COMMANDS"]

    if ctx.channel.id != mod_channel_id:
        await ctx.send(
            '<@{}> - You do not have permission to use that command here.'
            ''.format(ctx.author.id)
        )
        return False
    return True


def asyncless_is_moderator(ctx):
    """Version of is_moderator without async, for 'check' methods"""
    with open('server_specific/moderators.txt', 'r') as moderator_file:
        moderator_ids = moderator_file.read().splitlines()

    return str(ctx.author.id) in moderator_ids


def asyncless_is_mod_commands_channel(ctx):
    """Version without async, for 'check' methods"""
    with open('server_specific/channel_ids.json', 'r') as id_file:
        mod_channel_id = json.loads(id_file.read())["MOD_COMMANDS"]

    return ctx.channel.id == mod_channel_id


async def is_process_and_user_clear(bot, command, author_id):
    """Checks if a process is clear of a user, and vice versa"""
    # Check if user is in another process
    for user_id in bot.processes.values():
        if user_id == author_id:
            await ctx.send(
                '<@{}> - You are apparently already in another '
                'process.'.format(author_id)
            )
            return False

    # Check if someone is already in this process
    if 'm_make_wb' in bot.processes:
        if self.bot.processes['m_make_wb'] is not None:
            ctx.send(
                '<@{}> - Another user is busy in this process - please '
                'wait for the process to become free '
                'again.'.format(author_id)
            )
            return False

    # Otherwise, process must be clear
    return True


class ModeratorChecking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def m_list_moderators(self, ctx):
        if not await is_moderator(ctx):
            return

        if not await is_mod_commands_channel(ctx):
            return

        with open(Path('server_specific/moderators.txt'), 'r') as mod_file:
            moderator_ids = mod_file.readlines()

        for moderator_id in moderator_ids:
            moderator = self.bot.get_user(int(moderator_id))
            if not moderator:
                await ctx.send('Unknown')
            else:
                await ctx.send(moderator.name)
        await ctx.send('Finished!')
