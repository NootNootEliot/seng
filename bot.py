import discord
from discord.ext import commands
from pathlib import Path
import json
from cogs.greetings import Greetings
from cogs.send_welcome import Welcome
from cogs.validation import ModeratorChecking
from cogs.error_handler import CommandErrorHandler
from cogs.help import GetHelp
from cogs.member_stats import MemberStats
# from .validation import is_moderator, is_mod_commands_channel

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print("Ready to go!")

# Read in the token.
with open(Path('./private/priv_data.json'), 'r') as data_file:
    token = json.loads(data_file.read())['TOKEN']

bot.remove_command('help')  # Overwrite normal 'help' command
bot.add_cog(MemberStats(bot))
bot.add_cog(Greetings(bot))
bot.add_cog(Welcome(bot))
bot.add_cog(ModeratorChecking(bot))
bot.add_cog(GetHelp(bot))
bot.run(token)
