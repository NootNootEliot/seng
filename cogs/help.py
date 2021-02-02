from discord.ext import commands
from .validation import is_moderator, is_mod_commands_channel


class GetHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        help_string = (
            'All commands are prefixed with `$`.\n'
            '`hello` - Say \'hello\' to Seng!\n'
            '`privacy_policy` - View Seng\'s privacy policy.\n'
            '`source_code` - View Seng\'s source code.\n'
        )
        await ctx.send(help_string)

    @commands.command()
    async def m_help(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        help_string = (
            'These are the commands available to moderators. All commands'
            'are prefixed with `$`.\n'
            '`m_list_moderators` - List people with Seng moderator '
            'permissions.\n'
            '`m_help_welcome_blocks` - List information for using the welcome '
            'block.\n'
            '`m_help_stats` - List help information for using the `m_stats`'
            'functionality.\n'
        )
        await ctx.send(help_string)

    @commands.command()
    async def m_help_welcome_blocks(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        help_string = (
            'Below are the commands for the welcome block functionality. Note '
            'that the \'walkthrough processes\' can be cancelled at any time '
            'by writing \'cancel\'.\n'
            '`m_list_wb` - List the names of all welcome blocks that Seng has '
            'in storage.\n'
            '`m_make_wb` - Begin the walkthrough process of creating a '
            'welcome block.\n'
            '`m_remove_wb` - Begin the walkthrough process of instructing '
            'Seng to delete a welcome block.\n'
            '`m_preview_wb` - Begin the walkthrough process of previewing '
            'a single welcome block. Lets you see what it will look like!\n'
            '`m_view_wb_queue` - List the names of all welcome blocks that '
            'are currently in the welcome block queue.\n'
            '`m_add_wb_to_queue` - Begin the walkthrough process of adding a '
            'welcome block to the end of the queue.\n'
            '`m_insert_wb_in_queue` - Begin the walkthrough procecss of '
            'inserting a welcome block at a position in the queue.\n'
            '`m_remove_wb_from_queue` - Begin the walkthrough process of '
            'removing a welcome block from queue.\n'
            '`m_clear_wb_queue` - Clears the welcome block queue.\n'
            '`m_see_draft_welcome_message` - Seng will send the welcome '
            'messages, but in the mod-commands channel, so you can see '
            'what it will look like.\n'
            '`m_publish_welcome_message` - Seng will send the welcome '
            'messages, which correspond to those in the queue, to the '
            'welcome channel.\n\n'
            ''
            'To send a welcome message, it is first desirable to build the '
            'message out of \'blocks\', where \'blocks\' are effectively just '
            'messages. Blocks should be created through Seng. Blocks should '
            'then be added to the \'queue\' which is a collection of blocks '
            'for Seng to send. For this reason, you can create blocks that '
            'do not necessarily have to be in the queue - they can be kept '
            'around for later, for instance.\n'
            'If you would like to send media, please select the \'text\' '
            'option when making a welcome_blolck, and **paste** a **Discord**'
            ' link of the media.'
        )
        await ctx.send(help_string)

    @commands.command()
    async def m_help_stats(self, ctx):
        if not await is_moderator(ctx):
            return
        if not await is_mod_commands_channel(ctx):
            return

        help_string = (
            'Currently, `m_stats` refers to the persistent recording of '
            'how many members the server has in total, and how many of those '
            'members are online. Available commands are below:\n\n'
            '`m_stats_start` - Start the hourly recording of member counts.\n'
            '`m_stats_stop` - Stop the hourly recording of member counts.\n'
            '`m_stats_status` - Seng will inform you whether it\'s actively '
            'recording counts or not.\n'
            '`m_stats_show` - See a representation of the information that '
            'Seng has collected.\n'
            '`m_stats_clear` - Warning: This command will erase all `m_stats` '
            'data that Seng has in active storage.'
        )
        await ctx.send(help_string)
