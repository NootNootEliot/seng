from discord.ext import commands


class HallOfStars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Record the message count for each Member in server history
    async def record_baseline(self):
        pass

    # Start the message counting
    @commands.command()
    async def m_hos_start(self):
        pass
    
    # Stop the message counting
    @commands.command()
    async def m_hos_stop(self):
        pass
    
    # Restart the message counting
    @commands.command()
    async def m_hos_restart(self):
        pass
    
    # Outputs if messages are being recorded or not
    @commands.command()
    async def m_hos_status(self):
        pass
    
    # Force the Hall of Stars channel to update
    @commands.command()
    async def m_hos_force_update(self):
        pass
    
    # Update the Hall of Stars every 43200 seconds (12 hours)
    @tasks.loop(seconds=43200)
    async def hos_update(self):
        pass

    
