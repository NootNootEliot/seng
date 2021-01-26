import discord
from discord.ext import commands
from pathlib import Path
import json
from cogs.greetings import Greetings
from cogs.send_welcome import Welcome
from cogs.validation import ModeratorChecking
from cogs.error_handler import CommandErrorHandler
from cogs.help import GetHelp
from cogs.processes import Processes
from cogs.member_stats import MemberStats
from cogs.member_roles import MemberRoles
from cogs.channel_stats import ChannelStats
from cogs.seng_info import PrivacyPolicy

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=intents)

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
bot.add_cog(MemberStats(bot))
#bot.add_cog(MemberRoles(bot))
bot.add_cog(ChannelStats(bot))
bot.add_cog(Greetings(bot))
bot.add_cog(Welcome(bot))
bot.add_cog(ModeratorChecking(bot))
bot.add_cog(GetHelp(bot))
bot.add_cog(Processes(bot))
bot.add_cog(PrivacyPolicy(bot))
bot.run(token)
