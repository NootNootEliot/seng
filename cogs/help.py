from discord.ext import commands
from .validation import is_moderator, is_mod_commands_channel


class GetHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        help_string = (
            'All commands are prefixed with `$`.\n'
            '`hello` - Say \'hello\' to Seng!\n'
            '`privacy_policy` - View Seng\'s privacy policy.\n'
        )
        await ctx.send(help_string)

    @commands.command()
    async def m_help(self, ctx):
        if not await is_moderator(ctx):
            return

        if not await is_mod_commands_channel(ctx):
            return

        help_string = (
            'These are the commands available to moderators. All commands'
            'are prefixed with `$`.\n'
            'm_list_moderators - List people with Seng moderator permissions.'
        )
        await ctx.send(help_string)
