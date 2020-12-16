from discord.ext import commands


class Greetings(commands.Cog):
    def __init__(self, bot):
        pass

    @commands.command()
    async def hello(self, ctx):
        await ctx.channel.send('Hello <@{}>!'.format(ctx.author.id))
