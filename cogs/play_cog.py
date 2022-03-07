from __future__ import unicode_literals
import os
import threading

from discord.ext import commands
from .shared import vc, utils, queue,spotify_queuer


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
                tracks = await spotify_queuer.play_playlist(sound)
                url = utils.get_url(tracks[0])
                filename = ""
                if url is not None:
                    filename = utils.download(url, ctx, False)
                tracks.remove(tracks[0])
                track_list = []
                length = int(len(tracks))//6
                for x in range(len(tracks)):
                    track_list.append(tracks[x])
                    if x % length == 0 and x != 0:
                        download_thread = threading.Thread(target=utils.background_download, name="Downloader", args=(track_list,))
                        download_thread.start()
                        track_list = []
                if url is not None:
                    await vc.play(ctx.author.voice.channel, filename)


            else:
                filename = utils.download(sound, ctx)
                await ctx.send("Queuing " + (os.path.splitext(filename)[0]).split("sounds/")[1])
                await vc.play(ctx.author.voice.channel, filename)

        else:
            # check for file in the sounds folder
            filename = f"sounds/{sound}.mp3"

            if os.path.exists(filename):
                await vc.play(ctx.author.voice.channel, filename)

            else:
                url = utils.get_url(sound)

                if url is not None:
                    await ctx.send("Result Found. Preparing...")
                    filename = utils.download(url, ctx)
                    await ctx.send("Queuing " + (os.path.splitext(filename)[0]).split("sounds/")[1])
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

    @commands.command(name='shuffle', description='shuffles queue', pass_context=True)
    async def shuffle(self, ctx):
        await queue.shuffle()
        await ctx.send(":thumbsup:")

    @commands.command(name='top', description='queues to the top', pass_context=True)
    async def top(self, ctx, *, sound: str):
        url = utils.get_url(sound)
        filename = ""
        if url is not None:
            filename = utils.download(url, ctx, False)
        queue.queue.insert(1, filename)

    @commands.command(name='move', description='moves 2 indexes', pass_context=True)
    async def mov(self, ctx, *, sound: str):
        try:
            indexs = sound.split(" ")
            index1 = int(indexs[0])
            index2 = int(indexs[1])
            temp = queue.queue[index1]
            queue.queue[index1] = queue.queue[index2]
            queue.queue[index2] = temp
            await ctx.send("Moved Successfully")
        except TypeError:
            await ctx.send("Your slow")





