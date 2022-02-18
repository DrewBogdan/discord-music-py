from __future__ import unicode_literals
import os
import discord
from discord import client
from discord.ext import commands
from .shared import vc
import youtube_dl
import yt_dlp
import asyncio


class Play(commands.Cog):

    playing = False
    queue = []

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='play', description='play a sound', pass_context=True)
    async def play(self, ctx, sound):
        if not self.playing:
            self.playing = True
            filename = sound
            if "sounds" not in sound:
                filename = f"sounds/{sound}.mp3"
            if os.path.exists(filename):
                await vc.join_and_play(ctx.author.voice.channel, filename)
            elif "http" in sound:
                voice_state = ctx.author.voice

                if voice_state is None:
                    # Exiting if the user is not in a voice channel
                    return await ctx.send(f"get in a channel idiot")
                else:

                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                    'outtmpl':f"sounds" + '/%(title)s.%(ext)s',
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(sound, download=True)
                        file = ydl.prepare_filename(info).split("\\")[1]
                        filename = f"sounds/" + file.split(".webm")[0] + ".mp3"


                    if os.path.exists(filename):
                        await ctx.send("Joining")
                        await vc.join_and_play(ctx.author.voice.channel, filename)
                        # sets the playing back to false when done
                        self.playing = False
                        # takes the next song and plays it in the queue
                        if len(self.queue) > 0:
                            playing = self.queue[0]
                            self.queue.remove(playing)
                            await asyncio.sleep(2)
                            await self.play(ctx, playing)

                    else:
                        await ctx.send("Shits broke")
            else:
                await ctx.send(f"file not found: {filename}")
        else:
            await ctx.send("queueing")
            # the idea of this part is to download them once
            # they are added to the queue so when it runs into the main
            # play function its quicker
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'outtmpl': f"sounds" + '/%(title)s.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(sound, download=True)
                file = ydl.prepare_filename(info).split("\\")[1]
                filename = f"sounds/" + file.split(".webm")[0] + ".mp3"
            self.queue.append(filename)


    @commands.command(name='sounds', description='List availible sounds', pass_context=True)
    async def list(self, ctx):
        res = '```'
        for f in [os.path.splitext(filename)[0] for filename in os.listdir("sounds")]:
            res += f + '\n'

        res += "```"
        await ctx.send(res)

    @commands.command(name='stop', description='Stops music', pass_context=True)
    async def stop(self, ctx):
        await ctx.send("Im fuckin DEAD")
        server = ctx.message.guild.voice_client
        await server.disconnect()
