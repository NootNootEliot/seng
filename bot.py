import discord
from discord.ext import commands
from pathlib import Path
import json
from cogs.greetings import Greetings
from cogs.send_welcome import Welcome
from cogs.validation import ModeratorChecking
from cogs.error_handler import CommandErrorHandler
from cogs.help import GetHelp

bot = commands.Bot(command_prefix='$')

# Seng should keep track of which users are using which of Seng's processes,
# as some processes may only be 'user-safe' with a single user. We track this
# dictionary of 'task: user_id' in a bot constant called 'processes'.
bot.processes = {}


@bot.event
async def on_ready():
    print("Ready to go!")


# Read in the token.
with open(Path('./private/priv_data.json'), 'r') as data_file:
    token = json.loads(data_file.read())['TOKEN']

bot.remove_command('help')  # Overwrite normal 'help' command
#bot.add_cog(CommandErrorHandler(bot))
bot.add_cog(Greetings(bot))
bot.add_cog(Welcome(bot))
bot.add_cog(ModeratorChecking(bot))
bot.add_cog(GetHelp(bot))
bot.run(token)
