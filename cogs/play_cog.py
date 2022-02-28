from __future__ import unicode_literals
import os
from discord.ext import commands
from .shared import vc, utils


class Play(commands.Cog):

    playing = False
    queue = []

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='play', description='play a sound, new version', pass_context=True, aliases=['p'])
    async def play(self, ctx, *, sound: str):
        voice_state = ctx.author.voice

        if voice_state is None:
            # Exiting if the user is not in a voice channel
            return await ctx.send(f"get in a channel idiot")
        elif "https" in sound:
            # gets the link downloaded
            filename = await utils.download(sound, ctx)
            await vc.join_and_play(ctx.author.voice.channel, filename)
            os.remove(filename)
        else:
            # check for file in the sounds folder
            filename = f"sounds/{sound}.mp3"
            if os.path.exists(filename):
                await vc.join_and_play(ctx.author.voice.channel, filename)
            else:
                url = await utils.get_url(sound)
                await ctx.send("Search result: ")
                if url is not None:
                    filename = await utils.download(sound, ctx)
                    await vc.join_and_play(ctx.author.voice.channel, filename)
                    os.remove(filename)

    @commands.command(name='sounds', description='List availible sounds', pass_context=True)
    async def list(self, ctx):
        res = '```'
        for f in [os.path.splitext(filename)[0] for filename in os.listdir("sounds")]:
            res += f + '\n'

        res += "```"
        await ctx.send(res)

    @commands.command(name='skip', description='Skips song', pass_context=True)
    async def skip(self, ctx):
        await ctx.send("Skipping current song")
        self.playing = False
        server = ctx.message.guild.voice_client
        await server.disconnect()

    """
    @commands.command(name='skip', description='skips song', pass_context=True)
    async def skip(self, ctx):
        await ctx.send("Attempting to skip")
        await vc.skip(ctx.author.voice.channel)
    """





