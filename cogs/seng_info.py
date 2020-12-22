import discord
from discord.ext import commands


class PrivacyPolicy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def privacy_policy(self, ctx):
        priv_pol_text = (
            'Seng currently collects data that authorised users of the Discord '
            'server feed to it to make the \'welcome message\' embeds. This '
            'data is user-submitted strings of text.'
        )

        priv_pol_embed = discord.Embed(
            title='Privacy Policy',
            description=priv_pol_text,
            colour=discord.Color.teal()
        )
        await ctx.send(embed=priv_pol)

    @commands.command()
    async def source_code(self, ctx):
        source_code_text = (
            'You can view my source code [here]'
            '(https://github.com/NootNootEliot/seng)!'
        )

        source_code_embed = discord.Embed(
            title='Seng\'s Source Code',
            description=source_code_text,
            colour=discord.Color.green()
        )
        await ctx.send(embed=source_code_embed)
