import discord
from discord.ext import commands
from pathlib import Path
import json
from cogs.greetings import Greetings
from cogs.send_welcome import Welcome
from cogs.validation import ModeratorChecking
from cogs.error_handler import CommandErrorHandler
from cogs.help import GetHelp
# from .validation import is_moderator, is_mod_commands_channel

# Add in intent to allow us to monitor member stats

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print("Ready to go!")

class MemberStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()

    async def mstats(self, ctx):

        #if not await is_moderator(ctx):
        #    return
        #if not await is_mod_commands_channel(ctx):
        #    return

        with open('./server_specific/channel_ids.json', 'r') as id_file:
            channel_id_dict = json.loads(id_file.read())
            
            guild_id = channel_id_dict['GUILD']
            welcome_id = channel_id_dict['WELCOME']
            mbc_id = channel_id_dict['MOD_COMMANDS']

            guild = self.bot.get_guild(guild_id)
            welcome_channel = guild.get_channel(welcome_id)
     
            true_member_count = 0
            member_online_count = 0

            async for member in guild.fetch_members(limit=None):
                if not member.bot:
                    true_member_count += 1
                    if member.status != "offline":
                        member_online_count += 1

            await ctx.send(f'Total members: {true_member_count}')
            await ctx.send(f'Online members: {member_online_count}')

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
