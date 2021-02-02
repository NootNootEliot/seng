from discord.ext import commands
from pathlib import Path
from .validation import (is_moderator, is_mod_commands_channel,
                         asyncless_is_moderator,
                         asyncless_is_mod_commands_channel,
                         is_process_and_user_clear)
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

    async def get_block_name(self):
    """Return the message containing the block name to do something with"""
        def check(m):
            return (
                asyncless_is_mod_commands_channel(m) and
                m.author.id == author_id and
                not m.content.startswith('$m')
            )

        # Get the message containing the block to add
        await ctx.send('What is the name of the block? Alternatively, write'
                       '\'cancel\' to cancel.')
        return await self.bot.wait_for('message', check=check)
    
    def check_block_exists(self, block_message):
        """Checks if a given block is in storage"""
        does_block_exist = False
        for welcome_block in os.listdir('server_specific/welcome_blocks'):
            if welcome_block.startswith('_'):  # Ignore _block_queue
                continue
            if add_block_msg.content == welcome_block.replace('.json', ''):
                does_block_exist = True
        return does_block_exist

    async def send_block(self, data_dict, channel):
        """Send requested block in the requested channel"""
        if data_dict['type'] == 'text':
            await channel.send(data_dict['text'])
        elif data_dict['type'] == 'embed':
            block_embed = discord.Embed.from_dict(data_dict['embed_dict'])
            await channel.send(embed=block_embed)

    async def is_wanting_cancel(self, message, command):
        if message.content == 'cancel':
            await message.channel.send('Cancelling the procecss.')
            self.bot.processes[command] = None
            return True
        return False

    @commands.command()
    async def m_list_wb(self, ctx):
        """Lists all Welcome Blocks that Seng has in storage"""
        # Validation
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
        if not send_string:
            send_string = 'No blocks currently in storage!'
        await ctx.send(send_string)

    @commands.command()
    async def m_make_wb(self, ctx):
        """Process for a user creating a Welcome Block"""
        # Validation
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        author_id = ctx.author.id
        if not await is_process_and_user_clear(self.bot, 'm_make_wb',
                                               author_id):
            return
        # Add user to the process
        self.bot.processes['m_make_wb'] = author_id

        def check(m):
            return (
                asyncless_is_mod_commands_channel(m) and
                m.author.id == author_id and
                not m.content.startswith('$m')
            )

        await ctx.send('You may write \'cancel\' at any time during this '
                       'proceses to cancel it.\nPlease enter a name to '
                       'reference the block: (Note that entering the name of '
                       'an existing block will overwrite it.)')
        name_msg = await self.bot.wait_for('message', check=check)
        if await self.is_wanting_cancel(name_msg, 'm_make_wb'):
            return
        while True:
            await ctx.send('Is this block a text type (normal text characters,'
                           ' including media links), or an embed type (the '
                           'Discord \'boxes\'? Please enter either \'embed\' '
                           'or \'text\'.')
            type_msg = await self.bot.wait_for('message', check=check)
            if await self.is_wanting_cancel(type_msg, 'm_make_wb'):
                return

            # Make sure that the type_msg is valid
            if type_msg.content not in ['text', 'embed']:
                await ctx.send('Please enter either \'text\' or \'embed\'.')
            else:
                break

        # Request further information depending on the type of block
        if type_msg.content == 'text':
            await ctx.send('Please enter and send the text that you would '
                           'like to compose for this block.')
            text_msg = await self.bot.wait_for('message', check=check)
            if await self.is_wanting_cancel(text_msg, 'm_make_wb'):
                return
        elif type_msg.content == 'embed':
            # Embed Title
            await ctx.send('Please enter the embed\'s title.')
            embed_title_msg = await self.bot.wait_for('message', check=check)
            if await self.is_wanting_cancel(embed_title_msg, 'm_make_wb'):
                return

            # Embed Description
            await ctx.send('Please enter the embed\'s description.')
            embed_descrip_msg = await self.bot.wait_for('message', check=check)
            if await self.is_wanting_cancel(embed_descrip_msg, 'm_make_wb'):
                return

            # Embed Colour
            while True:  # Loop until format is correct
                # Request RGB colour values
                is_val_error = False
                await ctx.send('Please enter the embed\'s colour in the form '
                               'R G B. For instance, \'52 235 152\'')
                colour_msg = await self.bot.wait_for('message', check=check)
                if await self.is_wanting_cancel(colour_msg, 'm_make_wb'):
                    return

                # Get individual RGB values
                rgb = colour_msg.content.split(' ')

                # Ensure that numbers are entered, rather than e.g. characters
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

        # Construct dictionary for block storage
        data_dict = {}
        data_dict['title'] = name_msg.content
        data_dict['type'] = type_msg.content
        if type_msg.content == 'text':
            data_dict['text'] = text_msg.content
        elif type_msg.content == 'embed':
            # Embeds have their own dictionary for embed information
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
    async def m_remove_wb(self, ctx):
        """Command for removing a welcome block from storage"""
        # Validation
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        author_id = ctx.author.id
        if not await is_process_and_user_clear(self.bot, 'm_remove_wb',
                                               author_id):
            return
        # Add user to the process
        self.bot.processes['m_remove_wb'] = author_id

        def check(m):
            return (
                asyncless_is_mod_commands_channel(m) and
                m.author.id == author_id and
                not m.content.startswith('$m')
            )

        # Get name of the block to delete
        await ctx.send('Please enter the name of the welcome block you would '
                       'like to delete from **storage**. Alternatively, write '
                       '\'cancel\' to cancel.')
        del_block_msg = await self.bot.wait_for('message', check=check)
        if await self.is_wanting_cancel(del_block_msg, 'm_remove_wb'):
            return

        # Try removing that block from storage
        try:
            os.remove(os.path.join('server_specific/welcome_blocks',
                                   del_block_msg.content + '.json'))
        except FileNotFoundError:
            await ctx.send('I could not find that block! Cancelling.')
            self.bot.processes['m_remvoe_wb'] = None
            return

        await ctx.send('Deleted that welcome block.')
        self.bot.processes['m_remove_wb'] = None

    @commands.command()
    async def m_edit_wb(self, ctx):
        """Edits a welcome block"""
        # Validation
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        if not await is_process_and_user_clear(self.bot, 'm_edit_wb',
                                               ctx.author.id):
            return
        # Add user to the process
        self.bot.processes['m_edit_wb'] = ctx.author.id

        # Get the message containing the block to edit
        edit_block_msg = await self.get_block_name(ctx)
        if await self.is_wanting_cancel(add_block_msg, 'm_edit_wb'):
            return
        
        # Make sure that the block wanting to be edited exists
        does_block_exist = check_block_exists(edit_block_msg)
        if not does_block_exist:
            await ctx.send('I could not find that block! Cancelling.')
            self.bot.processes['m_edit_wb'] = None
            return
        
        # Load the welcome block as a dictionary file
        with open(edit_block_msg.content + '.json', 'r') as edit_block_file:
            block_dict = json.loads(edit_block_file.read())
        
        # Edit loop
        while True:
            # Output available keys
            available_keys = 'Available information to edit is: '
            for key in block_dict:
                available_keys += key + ', '
            available_keys += (
                '\nPlease enter a key name to edit its field. Or enter
                '\'cancel\' to cancel, or \'done\' to save. If you want to '
                'edit an embed, select \'embed_dict\' as the key. Then, copy '
                'and paste the existing value, and make your changes.'
            )
            await ctx.send(available_keys)

            def check(m):
                return (
                    asyncless_is_mod_commands_channel(m) and
                    m.author.id == author_id and
                    not m.content.startswith('$m')
                )
            # Get the message containing the key to edit
            key_message = await self.bot.wait_for('message', check=check)
            if await self.is_wanting_cancel(key_message, 'm_edit_wb'):
                return
            if key_message.content == 'done':
                # Write the new dictionary to the block file
                with open(edit_block_msgn.content + '.json', 'w') as e_b_file:
                    e_b_file.write(json.dumps(block_dict))
                await ctx.send('Saved your changes.')
                self.bot.processes['m_edit_wb'] = None

            # Check that the key is actually in the available keys
            if key_message.content not in block_dict.keys():
                await ctx.send('I do not recognise that key. Please enter one '
                               'of the available keys listed above.')
                continue
            if key_message.content == 'title':
                await ctx.send('Please do not change the title of the block, '
                               'as this may interfere with functionality.')
                continue
            
            # Ask for the new requested value
            await ctx.send(
                'Please enter the new value that you would like to replace '
                'the existing one with. The existing value '
                'is: {}'.format(block_dict[key_message.content])
            )
            replace_message = await self.bot.wait_for('message', check=check)
            if await self.is_wanting_cancel(replace_message, 'm_edit_wb'):
                return
            
            # Replace the existing value with the new one.
            block_dict[key_message.content] = replace_message.content
            await ctx.send('Replaced existing value.')

    @commands.command()
    async def m_preview_wb(self, ctx):
        """User requests a Welcome Block to view"""
        # Validation
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        author_id = ctx.author.id
        if not await is_process_and_user_clear(self.bot, 'm_preview_wb',
                                               author_id):
            return False
        self.bot.processes['m_preview_wb'] = author_id

        # The check used for correspondance with the user
        def check(m):
            return (
                asyncless_is_mod_commands_channel(m) and
                m.author.id == author_id and
                not m.content.startswith('$m')
            )

        # Ask for the name of the block to preview
        await ctx.send('What block would you like to search for to preview? '
                       'Alternatively, write \'cancel\' to cancel.')
        name_msg = await self.bot.wait_for('message', check=check)
        if await self.is_wanting_cancel(name_msg, 'm_preview_wb'):
            return

        # Path must be the requested name, plus the .json file extension
        block_path = os.path.join(
                'server_specific/welcome_blocks',
                name_msg.content + '.json'
        )

        # Try opening the block file to send it
        try:
            with open(Path(block_path), 'r') as block_file:
                data_dict = json.loads(block_file.read())
            await self.send_block(data_dict, ctx)
        except FileNotFoundError:
            await ctx.send('I could not find that block! Cancelling.')

        self.bot.processes['m_preview_wb'] = None

    @commands.command()
    async def m_clear_wb_queue(self, ctx):
        """Clears the welcome block queue"""
        # Validation
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        
        # Open the file and close it to erase it
        block_queue_path = 'server_specific/welcome_blocks/_block_queue'
        open(block_queue_path, 'w').close()
        await ctx.send('Cleared welcome block queue.')

    @commands.command()
    async def m_view_wb_queue(self, ctx):
        """Print the current Welcome Block queue"""
        # Validation
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
        """Adds requested Welcome Block to the end of the queue"""
        # Validation
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        if not await is_process_and_user_clear(self.bot, 'm_add_wb_to_queue',
                                               ctx.author.id):
            return
        # Add user to the process
        self.bot.processes['m_add_wb_to_queue'] = ctx.author.id

        # Get the message containing the block to add
        add_block_msg = await self.get_block_name(ctx)
        if await self.is_wanting_cancel(add_block_msg, 'm_add_wb_to_queue'):
            return

        # Make sure that the block wanting to be added exists
        does_block_exist = check_block_exists(add_block_msg)
        if not does_block_exist:
            await ctx.send('I could not find that block! Cancelling.')
            self.bot.processes['m_add_wb_to_queue'] = None
            return

        # Append block to the end of the block queue file
        block_queue_path = 'server_specific/welcome_blocks/_block_queue'
        with open(Path(block_queue_path), 'a+') as block_queue_file:
            block_queue_file.write(add_block_msg.content + '\n')

        await ctx.send('Added block to the queue!')
        self.bot.processes['m_add_wb_to_queue'] = None

    @commands.command()
    async def m_insert_wb_in_queue(self, ctx):
        """Inserts a welcome block at a position in the queue"""
        # Validation
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        if not await is_process_and_user_clear(self.bot, 'm_add_wb_to_queue',
                                               ctx.author.id):
            return

        # Add user to the process
        self.bot.processes['m_insert_wb_in_queue'] = ctx.author.id

        # Get the message containing the block to insert
        insert_block_msg = await self.get_block_name(ctx)
        if await self.is_wanting_cancel(add_block_msg, 'm_insert_wb_in_queue'):
            return
        
        # Make sure that the block wanting to be inserted exists
        does_block_exist = check_block_exists(insert_block_msg)
        if not does_block_exist:
            await ctx.send('I could not find that block! Cancelling.')
            self.bot.processes['m_insert_wb_in_queue'] = None
            return
        
        # Position to insert
        def check(m):
            return (
                asyncless_is_mod_commands_channel(m) and
                m.author.id == author_id and
                not m.content.startswith('$m')
            )
        
        # Get the message containing the insert position
        await ctx.send(
            'At what position should I insert this block into the queue? '
            'Please enter an integer number, which will be the **position** '
            'of the block in the queue, where the starting position is 1. '
            'Alternatively, write \'cancel\' to cancel.'
        )
        insert_position_msg = await self.bot.wait_for('message', check=check)
        if await self.is_wanting_cancel(insert_position_msg,
                                        'm_insert_wb_in_queue'):
            return
        
        pos = insert_position_msg.content
        # Check that the insert position is a digit
        if not pos.isdigit():
            await ctx.send(
                'Please send an integer number.\nCancelling.'
                self.bot.processes['m_insert_wb_in_queue'] = None
                return
            )
        
        # Get length of welcome block queue for bound checking
        block_queue_path = 'server_specific/welcome_blocks/_block_queue'
        with open(Path(block_queue_path), 'r') as block_queue_file:
            blocks = block_queue_file.read().splitlines()
            length = len(blocks)

        # Check that the integer is within the correct bounds
        if (int(pos.content) < 1) or (int(pos.content) > length + 1)
             await ctx.send(
                'Please enter an integer number between 1 and the length of '
                'the welcome block queue (plus one).\nCancelling.'
                self.bot.processes['m_insert_wb_in_queue'] = None
                return
            )
        
        # Insert block
        # Erase the entire queue file
        open(block_queue_path, 'w').close()

        # Rewrite the queue, inserting the block
        with open(block_queue_path, 'a') as block_queue_file:
            for counter, block in enumerate(blocks):
                # Check to insert the block
                if counter + 1 == int(pos.content):
                    block_queue_file.write(insert_block_msg.content + '\n')
                block_queue_file.write(block + '\n')
        await ctx.send('Block inserted.')
        self.bot.processes['m_insert_wb_in_queue'] = None

    @commands.command()
    async def m_remove_wb_from_queue(self, ctx):
        """Remove a requested Welcome Block from queue"""
        # Validation
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return
        if not await is_process_and_user_clear(self.bot,
                                               'm_remove_wb_from_queue',
                                               ctx.author.id):
            return
        # Add user to the process
        self.bot.processes['m_remove_wb_from_queue'] = ctx.author.id

        # Get the message containing the block to remove
        rem_block_msg = await self.get_block_name(ctx)
        if is_wanting_cancecl(rem_block_msg, 'm_remove_wb_from_queue'):
            return

        # Read the file before erasing
        block_queue_path = 'server_specific/welcome_blocks/_block_queue'
        with open(Path(block_queue_path), 'r') as block_queue_file:
            blocks = block_queue_file.read().splitlines()

        # Erase the entire queue file
        open(block_queue_path, 'w').close()

        # Write all blocks back to the file, except for the removed block
        with open(Path(block_queue_path), 'a') as block_queue_file:
            for block in blocks:
                if block == rem_block_msg.content:
                    continue
                block_queue_file.write(block + '\n')
        await ctx.send('Block removed.')
        self.bot.processes['m_remove_wb_from_queue'] = None

    @commands.command()
    async def m_see_draft_welcome_message(self, ctx):
        """Print the current Welcome Block queue in 'export' form"""
        # Validation
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        # Get the 'blocks' in queue
        block_queue_path = 'server_specific/welcome_blocks/_block_queue'
        with open(Path(block_queue_path), 'r') as block_queue_file:
            blocks = block_queue_file.read().splitlines()

        # Open each block in the queue, and send it
        for block in blocks:
            block_path = os.path.join(
                'server_specific/welcome_blocks',
                block + '.json'
            )
            with open(Path(block_path), 'r') as block_file:
                data_dict = json.loads(block_file.read())

            await self.send_block(data_dict, ctx)

    @commands.command()
    async def m_publish_welcome_message(self, ctx):
        """Send the Welcome Block queue into the welcome channel"""
        # Validation
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        author_id = ctx.author.id
        if not await is_process_and_user_clear(self.bot,
                                               'm_publish_welcome_message',
                                               author_id):
            return
        # Add user to the process
        self.bot.processes['m_publish_welcome_message'] = author_id

        def check(m):
            return (
                asyncless_is_mod_commands_channel(m) and
                m.author.id == author_id and
                not m.content.startswith('$m')
            )

        # Confirmation check
        await ctx.send('Are you sure that you want to publish the welcome '
                       'message? This will be posted publicly in the welcome '
                       'message channel. Please enter either \'yes\' or '
                       '\'no\'.')
        while True:
            yes_no_msg = await self.bot.wait_for('message', check=check)
            if await self.is_wanting_cancel(yes_no_msg,
                                            'm_publish_welcome_message'):
                return
            if yes_no_msg.content not in ['yes', 'no', 'cancel']:
                await ctx.send('Please enter either \'yes\' or \'no\'.')
                continue
            break

        if yes_no_msg.content == 'no':
            await ctx.send('Cancelling.')
            self.bot.processes['m_publish_welcome_message'] = None
            return

        # Otherwise, yes_no_msg.content is 'yes'

        # Get a list of all the blocks in the queue
        block_queue_path = 'server_specific/welcome_blocks/_block_queue'
        with open(Path(block_queue_path), 'r') as block_queue_file:
            blocks = block_queue_file.read().splitlines()

        # Get the welcome channel
        with open('server_specific/channel_ids.json', 'r') as id_file:
            channel_id_dict = json.loads(id_file.read())
            guild_id = channel_id_dict['GUILD']
            welcome_id = channel_id_dict['WELCOME']
        guild = self.bot.get_guild(guild_id)
        welcome_channel = guild.get_channel(welcome_id)

        # For every block in the queue, send it out
        for block in blocks:
            block_path = os.path.join(
                'server_specific/welcome_blocks',
                block + '.json'
            )
            with open(Path(block_path), 'r') as block_file:
                data_dict = json.loads(block_file.read())
            await self.send_block(data_dict, welcome_channel)

        self.bot.processes['m_publish_welcome_message'] = None
