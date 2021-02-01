from discord.ext import commands


class MuteMember(commands.Cog):
    """Class for commands related to muting Members"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mute_member():
        """Mutes a Member"""
        pass

    @commands.command()
    async def unmute_member():
        """Unmutes a Member"""
        pass

    @commands.command()
    async def view_muted_members():
        """Outputs a list of all Members who are muted"""
        pass

    @commands.command()
    async def mute_perm_setup():
        """Sets up the mute permission setting on every channel in the guild"""
