import os
import discord
from discord.ext import commands
from .shared import vc

class Play(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='play', description='play a sound', pass_context=True)
    async def play(self, ctx, sound):
        filename = f"sounds/{sound}.mp3"
        if os.path.exists(filename):
            await vc.join_and_play(ctx.author.voice.channel, filename)
        else:
            await ctx.send(f"file not found: {filename}")

    @commands.command(name='sounds', description='List availible sounds', pass_context=True)
    async def list(self, ctx):
        res = '```'
        for f in [os.path.splitext(filename)[0] for filename in os.listdir("sounds")]:
            res += f + '\n'

        res += "```"
        await ctx.send(res)