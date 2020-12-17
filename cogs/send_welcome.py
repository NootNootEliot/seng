from discord.ext import commands
from pathlib import Path
from .validation import is_moderator, is_mod_commands_channel
import json
import os
import discord


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_block(data_dict, channel):
        if data_dict['type'] == 'text':
            await channel.send(data_dict['text'])
        elif data_dict['type'] == 'embed':
            block_embed = discord.Embed.from_dict(data_dict['embed_dict'])
            await channel.send(embed=block_embed)

    @commands.command()
    async def m_list_welcome_blocks(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        
        send_string = ''
        for welcome_block in os.listdir('server_specific/welcome_blocks'):
            if welcome_block.startswith('_'):
                continue
            send_string += welcome_block.replace('.json', '') + '\n'
            await ctx.send(send_string)

    @commands.command()
    async def m_make_welcome_block(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        
        await ctx.send('Please enter the name of the block:')
        def check(m):
            return True
        name_msg = await self.bot.wait_for('message', check=check)

        await ctx.send('What block is this? e.g. \'text\' or \'embed\'')
        type_msg = await self.bot.wait_for('message', check=check)

        if type_msg.content == 'text':
            await ctx.send('Please enter the text that you would like!')
            text_msg = await self.bot.wait_for('message', check=check)
        elif type_msg.content == 'embed':
            await ctx.send('Please enter the title of the embed.')
            embed_title_msg = await self.bot.wait_for('message', check=check)
            await ctx.send('Please enter the embed\'s description.')
            embed_descrip_msg = await self.bot.wait_for('message', check=check)
            await ctx.send('Please enter the colour for the embed.')
            colour_msg = await self.bot.wait_for('message', check=check)
        
        data_dict = {}
        data_dict['title'] = name_msg.content
        data_dict['type'] = type_msg.content
        if type_msg.content == 'text':
            data_dict['text'] = text_msg.content
        elif type_msg.content == 'embed':
            embed_dict = {}
            embed_dict['title'] = embed_title_msg.content
            embed_dict['description'] = embed_descrip_msg.content
            rgb_vals = colour_msg.content.split(' ')
            rgb = [int(val) for val in rgb_vals]
            colour = discord.Color.from_rgb(rgb[0], rgb[1], rgb[2])
            embed_dict['color'] = int(str(colour).lstrip('#'), 16)
            embed_dict['type'] = 'rich'
            data_dict['embed_dict'] = embed_dict
        block_path = os.path.join(
                'server_specific/welcome_blocks',
                name_msg.content + '.json'
        )
        with open(Path(block_path), 'w+') as block_file:
            block_file.write(json.dumps(data_dict))

        await ctx.send('Block formation process completed.')

    @commands.command()
    async def m_preview_welcome_block(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        await ctx.send('What block would you like to search for?')
        def check(m):
            return True
        name_msg = await self.bot.wait_for('message', check=check)
        block_path = os.path.join(
                'server_specific/welcome_blocks',
                name_msg.content + '.json'
        )
        with open(Path(block_path), 'r') as block_file:
            data_dict = json.loads(block_file.read())

        await send_block(data_dict, ctx)

    @commands.command()
    async def m_view_welcome_block_queue(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        block_queue_path = 'server_specific/welcome_blocks/_block_queue'
        with open(Path(block_queue_path), 'r') as block_queue_file:
            blocks = block_queue_file.readlines()
            if not blocks:
                await ctx.send('No blocks in queue!')
            for block in blocks:
                await ctx.send(block)

    @commands.command()
    async def m_add_welcome_block_to_queue(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        await ctx.send('What block would you like to add to the queue?')
        def check(m):
            return True
        add_block_msg = await self.bot.wait_for('message', check=check)
        block_queue_path = 'server_specific/welcome_blocks/_block_queue'
        with open(Path(block_queue_path), 'a+') as block_queue_file:
            block_queue_file.write(add_block_msg.content + '\n')

        await ctx.send('Added block to the queue!')

    @commands.command()
    async def m_see_draft_welcome_message(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        block_queue_path = 'server_specific/welcome_blocks/_block_queue'
        with open(Path(block_queue_path), 'r') as block_queue_file:
            blocks = block_queue_file.read().splitlines()

        for block in blocks:
            block_path = os.path.join(
                'server_specific/welcome_blocks',
                block + '.json'
            )
            with open(Path(block_path), 'r') as block_file:
                data_dict = json.loads(block_file.read())

            await send_block(data_dict, ctx)

    @commands.command()
    async def m_remove_welcome_block_from_queue(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        await ctx.send('What block would you like to remove from the queue?')
        def check(m):
            return True
        rem_block_msg = await self.bot.wait_for('message', check=check)
        block_queue_path = 'server_specific/welcome_blocks/_block_queue'
        with open(Path(block_queue_path), 'r') as block_queue_file:
            blocks = block_queue_file.read().splitlines()
        
        open(Path(block_queue_path), 'w').close()

        with open(Path(block_queue_path), 'a') as block_queue_file:
            for block in blocks:
                if block == rem_block_msg.content:
                    continue
                block_queue_file.write(block)
        await ctx.send('Block removed.')

    @commands.command()
    async def m_publish_welcome_message(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        block_queue_path = 'server_specific/welcome_blocks/_block_queue'
        with open(Path(block_queue_path), 'r') as block_queue_file:
            blocks = block_queue_file.read().splitlines()

        with open('server_specific/channel_ids.json', 'r') as id_file:
            channel_id_dict = json.loads(id_file.read())
            guild_id = channel_id_dict['GUILD']
            welcome_id = channel_id_dict['WELCOME']

        guild = self.bot.get_guild(guild_id)
        welcome_channel = guild.get_channel(welcome_id)

        for block in blocks:
            block_path = os.path.join(
                'server_specific/welcome_blocks',
                block + '.json'
            )
            with open(Path(block_path), 'r') as block_file:
                data_dict = json.loads(block_file.read())

            await send_block(data_dict, welcome_channel)
