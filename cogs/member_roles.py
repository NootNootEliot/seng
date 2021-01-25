import discord
from discord.ext import tasks, commands
from pathlib import Path
from .validation import (is_moderator, is_mod_commands_channel,
                         asyncless_is_moderator,
                         asyncless_is_mod_commands_channel,
                         is_process_and_user_clear)
import json
import os
from os import path


class MemberRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.response_reference = 0
        self.responses = ["Great introduction ",
                          "Thank you for introducing yourself ",
                          "Glad to have you onboard ",
                          "Nothing like an introduction ",
                          "Look foward to seeing more of you "]

        with open('./server_specific/channel_ids.json', 'r') as id_file:
            channel_id_dict = json.loads(id_file.read())
            self.guild_id = channel_id_dict['GUILD']
            self.meet_our_members_id = channel_id_dict['MEET_OUR_MEMBERS']

    def cog_unload(self):
        self.m_roles.cancel()

    @commands.Cog.listener()
    async def on_message(self, message):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        if message.channel.id == self.meet_our_members_id:
            if not message.author.bot:
                msg = message
                self.response_reference += 1
                if self.response_reference > (len(self.responses) - 1):
                    self.response_reference = 0
                announcement = self.responses[self.response_reference] + \
                    message.author.name + "!"
                await message.channel.send(announcement)
                tourist_role = discord.utils.get(message.guild.roles,
                                                 name="Tourist")
                resident_role = discord.utils.get(message.guild.roles,
                                                  name="Resident")
                announcement = "\U0001F973" \
                    " Congratulations! You are now a Resident!"
                for role in message.author.roles:
                    if role.name == "Tourist":
                        await message.author.remove_roles(tourist_role)
                        await message.author.add_roles(resident_role)
                        await message.channel.send(announcement)
        return
