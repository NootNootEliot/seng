import discord
from discord.ext import commands
from pathlib import Path
import json
from cogs.greetings import Greetings
from cogs.send_welcome import Welcome
from cogs.validation import ModeratorChecking
from cogs.error_handler import CommandErrorHandler
from cogs.help import GetHelp

# Add intent to allow bot to monitor member stats
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print("Ready to go!")
        
    # -------------------------------------------
    # List ALL 'online' member
    # -------------------------------------------

    # guild_name = "ExplorerTest"
    guild_name = "Astra Nova Network"

    for guild in bot.guilds:
        if guild.name == guild_name:
            break

    true_member_count = 0
    member_online_count = 0

    async for member in guild.fetch_members(limit=None):
        # print(member)
        if not member.bot:
            # print(member) - lists all non bot members
            true_member_count += 1
            if member.status != "offline":
                member_online_count += 1
    print(f'Total true member count: {true_member_count}')
    print(f'Online member count: {member_online_count}')

    # ---------------------------------------------
    #
    # ---------------------------------------------


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
