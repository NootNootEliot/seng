from discord.ext import commands
from pathlib import Path
from .validation import (is_moderator, is_mod_commands_channel,
        asyncless_is_moderator, asyncless_is_mod_commands_channel)
import json
import os
import discord


class Welcome(commands.Cog):
    """Class for the Welcome Message command collection

    Welcome Blocks are effectively files of json data that contain the
    necesesary information to compose the Welcome Block and send it.

    This class contains methods which allow moderators to write Welcome Blocks,
    draft them into message queues, send them out into the #welcome channel,
    and other support commands.
    """
    def __init__(self, bot):
        self.bot = bot

    async def send_block(self, data_dict, channel):
        """Send requested block in the requested channel"""
        if data_dict['type'] == 'text':
            await channel.send(data_dict['text'])
        elif data_dict['type'] == 'embed':
            block_embed = discord.Embed.from_dict(data_dict['embed_dict'])
            await channel.send(embed=block_embed)

    @commands.command()
    async def m_list_wb(self, ctx):
        """Lists all Welcome Blocks that Seng has in storage"""
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        
        send_string = ''
        for welcome_block in os.listdir('server_specific/welcome_blocks'):
            if welcome_block.startswith('_'):  # Ignore _block_queue
                continue
            # Get just the name, and add a newline to separate the filenames
            send_string += welcome_block.replace('.json', '\n')
        await ctx.send(send_string)

    @commands.command()
    async def m_make_wb(self, ctx):
        """Process for a user creating a Welcome Block"""
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        author_id = ctx.author.id
        # Check if user is in another process
        for user_id in self.bot.processes.values():
            if user_id == author_id:
                await ctx.send(
                    '<@{}> - You are apparently already in another '
                    'process.'.format(author_id)
                )
                return

        # Check if someone is already in this process 
        if 'm_make_wb' in self.bot.processes:
            if self.bot.processes['m_make_wb'] != None:
                ctx.send(
                    '<@{}> - Another user is busy in this process - please '
                    'wait for the process to become free '
                    'again.'.format(author_id)
                )
                return

        # Add user to the process
        self.bot.processes['m_make_wb'] = author_id

        await ctx.send('Please enter a name to reference the block:')

        def check(m):
            return (
                asyncless_is_moderator(m) and
                asyncless_is_mod_commands_channel(m) and
                not m.content.startswith('$m')
            )

        name_msg = await self.bot.wait_for('message', check=check)
        while True:
            await ctx.send('Is this block a text type (normal text characters, '
                           'including media links), or an embed type (the '
                           'Discord \'boxes\'? Please enter either \'embed\' '
                           'or \'text\'.')
            type_msg = await self.bot.wait_for('message', check=check)
            
            # Make sure that the type_msg is valid
            if type_msg.content not in ['text', 'embed']:
                await ctx.send('Please enter either \'text\' or \'embed\'.')
            else:
                break

        if type_msg.content == 'text':
            await ctx.send('Please enter and send the text that you would '
                           'like to compose for  this block.')
            text_msg = await self.bot.wait_for('message', check=check)
        elif type_msg.content == 'embed':
            await ctx.send('Please enter the embed\'s title.')
            embed_title_msg = await self.bot.wait_for('message', check=check)
            await ctx.send('Please enter the embed\'s description.')
            embed_descrip_msg = await self.bot.wait_for('message', check=check)

            while True:
                is_val_error = False
                await ctx.send('Please enter the embed\'s colour in the form '
                               'R G B. For instance, \'52 235 152\'')
                colour_msg = await self.bot.wait_for('message', check=check)
                # Get individual RGB values
                rgb = colour_msg.content.split(' ')

                # Ensure that numbers are entered
                try:
                    colour = discord.Color.from_rgb(int(rgb[0]), int(rgb[1]),
                                                    int(rgb[2]))
                except ValueError:
                    await ctx.send('Error - incorrect format.')
                    continue

                # Ensure that entered numbers are in the correct range
                for val in rgb:
                    if (int(val) > 255) or (int(val) < 0):
                        await ctx.send('Error - RGB values musut be between 0 '
                                       'and 255 inclusive.')
                        is_val_error = True
                        break
                if is_val_error:
                    continue
                break
        
        data_dict = {}
        data_dict['title'] = name_msg.content
        data_dict['type'] = type_msg.content
        if type_msg.content == 'text':
            data_dict['text'] = text_msg.content
        elif type_msg.content == 'embed':
            embed_dict = {}
            embed_dict['title'] = embed_title_msg.content
            embed_dict['description'] = embed_descrip_msg.content

            # Edit the colour for storage use
            embed_dict['color'] = int(str(colour).lstrip('#'), 16)
            
            # 'rich ' is the default
            embed_dict['type'] = 'rich'
            data_dict['embed_dict'] = embed_dict

        block_path = os.path.join('server_specific/welcome_blocks',
                                  name_msg.content + '.json')
        with open(Path(block_path), 'w+') as block_file:
            block_file.write(json.dumps(data_dict))

        await ctx.send('Block formation process completed. Thank you!')

        # Free user from process and free process from user
        self.bot.processes['m_make_wb'] = None

    @commands.command()
    async def m_preview_wb(self, ctx):
        """User requests a Welcome Blolck to view"""
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        await ctx.send('What block would you like to search for?')
        def check(m):
            return True
        name_msg = await self.bot.wait_for('message', check=check)
        # Path must be the requested name, plus the .json file extension
        block_path = os.path.join(
                'server_specific/welcome_blocks',
                name_msg.content + '.json'
        )
        with open(Path(block_path), 'r') as block_file:
            data_dict = json.loads(block_file.read())

        await self.send_block(data_dict, ctx)

    @commands.command()
    async def m_view_wb_queue(self, ctx):
        """Print the current Welcome Block queue"""
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
    async def m_add_wb_to_queue(self, ctx):
        """Add requested Welcome Block to the queue"""
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
        """Print the current Welcome Block queue in 'export' form"""
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

            await self.send_block(data_dict, ctx)

    @commands.command()
    async def m_remove_wb_from_queue(self, ctx):
        """Remove a requested Welcome Block from queue"""
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
        
        open(Path(block_queue_path), 'w').close()  # Erase entire file

        with open(Path(block_queue_path), 'a') as block_queue_file:
            for block in blocks:
                if block == rem_block_msg.content:
                    continue
                block_queue_file.write(block + '\n')
        await ctx.send('Block removed.')

    @commands.command()
    async def m_publish_welcome_message(self, ctx):
        """Send the Welcome Block queue into the welcome channel"""
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

            await self.send_block(data_dict, welcome_channel)
