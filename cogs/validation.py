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
