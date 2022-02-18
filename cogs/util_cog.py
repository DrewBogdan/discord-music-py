from __future__ import unicode_literals
import os
import sys
import asyncio
import discord
from discord import client
from discord.ext import commands

from .shared import vc

class Util(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='gotobed', description='Sends the bot away', pass_context=True)
    async def kill(self, ctx):
        if ctx.author == "230106342994608129":
            await ctx.send(":sleeping_accommodation:")
            self.playing = False
            server = ctx.message.guild.voice_client
            await server.disconnect()
            sys.exit()




