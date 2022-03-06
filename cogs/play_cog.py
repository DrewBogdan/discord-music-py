from __future__ import unicode_literals
import os
from discord.ext import commands
from .shared import vc, utils, queue


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
            if "open.spotify.com" in sound:
                await ctx.send("That is a spotify playlist")

            else:
                filename = await utils.download(sound, ctx)
                await vc.play(ctx.author.voice.channel, filename)

        else:
            # check for file in the sounds folder
            filename = f"sounds/{sound}.mp3"

            if os.path.exists(filename):
                await vc.play(ctx.author.voice.channel, filename)

            else:
                url = await utils.get_url(sound)

                if url is not None:
                    await ctx.send("Result Found. Preparing...")
                    filename = await utils.download(url, ctx)
                    await vc.play(ctx.author.voice.channel, filename)

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

    @commands.command(name='stop', description='halts all playing', pass_context=True)
    async def stop(self, ctx):
        self.playing = False
        server = ctx.message.guild.voice_client
        await queue.clear_queue()
        await server.disconnect()

    @commands.command(name='queue', description='prints song queue', pass_context=True, aliases=['q'])
    async def queue(self, ctx):
        await ctx.send("Current Queue:")
        await ctx.send("-------------------------------------------------")
        await queue.print_queue(ctx)

    @commands.command(name='remove', description='removes given song from queue', pass_context=True, aliases=['rm'])
    async def remove(self, ctx, index):
        if len(queue.queue) > int(index) > 0:
            val = await queue.remove_from_queue(int(index))
            await ctx.send("Removed " + val + " from queue")
        else:
            await ctx.send("Invalid")





