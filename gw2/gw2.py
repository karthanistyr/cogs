import discord
import requests
from discord.ext import commands

class gw2:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def characters(self, ctx):
        """This does stuff!"""

        #Your code will go here
        print(self)
        await self.bot.say("I can do stuff to" + ctx.message.author.mention  + "!")

def setup(bot):
    bot.add_cog(gw2(bot))
