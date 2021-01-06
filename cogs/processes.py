from discord.ext import commands
from .validation import is_moderator, is_mod_commands_channel


class Processes(commands.Cog):
    """Class for commands relating to Processes"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def m_view_active_processes(self, ctx):
        """
        Print a representation of active processes and associated members to
        the channel.
        """
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        # If dictionary is empty
        processes_dict = self.bot.processes
        if bool(processes_dict) == False:
            await ctx.send('There are no active processes!') 
            return
        else:
            send_string = ''  # Build the string from nothing
            for process in processes_dict:
                user = await self.bot.fetch_user(processes_dict[process])
                send_string += '`{}`: {}\n'.format(process, user.name)
            await ctx.send(send_string)
