from __future__ import unicode_literals
import os
import discord
from discord import client
from discord.ext import commands
from .shared import vc
import youtube_dl

class Play(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='play', description='play a sound', pass_context=True)
    async def play(self, ctx, sound):
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
                        'preferredquality': '96',
                    }],
                    'outtmpl':f"sounds/" + '/1.%(ext)s',
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([sound])
                filename = f"sounds/1.mp3"
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

    @commands.command(name='stop', description='Stops music', pass_context=True)
    async def stop(self, ctx):
        await ctx.send("Im fuckin DEAD")
        server = ctx.message.guild.voice_client
        await server.disconnect()
