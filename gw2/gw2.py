import discord
import requests
from discord.ext import commands

class gw2:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.commandIssuer = ctx.message.author
        self.bot = bot

    @commands.command()
    async def characters(self):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("I can do stuff to" + commandIssue.mention  + "!")

def setup(bot):
    bot.add_cog(gw2(bot))
