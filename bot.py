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
from cogs.mute_member import MuteMember

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=intents)

# Seng should keep track of which users are using which of Seng's processes,
# as some processes may only be 'user-safe' with a single user. We track this
# dictionary of 'task: user_id' in a bot constant called 'processes'.
bot.processes = {}


@bot.event
async def on_ready():
    print("Ready to go!")

    # Get Seng's ID
    # Get the mod-commands channel
    with open('server_specific/channel_ids.json', 'r') as id_file:
        channel_id_dict = json.loads(id_file.read())
        guild_id = channel_id_dict['GUILD']
        mod_commands_id = channel_id_dict['MOD_COMAMANDS']
    guild = self.bot.get_guild(guild_id)
    mod_commands_channel = guild.get_channel(mod_commands_id)

    # Send a message to the mod-commands channel
    msg = await mod_commands_channel.send('I am online!')
    
    # Store Seng's ID in a bot constant
    bot.my_id = msg.author.id


# Read in the token.
with open(Path('./private/priv_data.json'), 'r') as data_file:
    token = json.loads(data_file.read())['TOKEN']

bot.remove_command('help')  # Overwrite normal 'help' command
# bot.add_cog(CommandErrorHandler(bot))
bot.add_cog(MemberStats(bot))
# bot.add_cog(MemberRoles(bot))
bot.add_cog(ChannelStats(bot))
bot.add_cog(Greetings(bot))
bot.add_cog(Welcome(bot))
bot.add_cog(ModeratorChecking(bot))
bot.add_cog(GetHelp(bot))
bot.add_cog(Processes(bot))
bot.add_cog(PrivacyPolicy(bot))
bot.add_cog(MuteMember(bot))
bot.run(token)
