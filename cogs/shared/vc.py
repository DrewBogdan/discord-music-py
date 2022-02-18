'''
Utilities for interacting with voice channels
'''

import asyncio
import os

import discord

VC_LOCK = asyncio.Lock()
Skip = False

async def join_and_play(channel, file):
    """
    Connects to the given voice channel, playing the given .mp3 file
    over voice, before disconnecting

    Args:
        channel (VoiceChannel): Voice Channel to connect to
        file (str): path to .mp3 file to play
    """


    async with VC_LOCK:
        conn = await channel.connect()
        # executable=("C:\Program Files (x86)\\ffmpeg-master-latest-win64-gpl\\bin"))
        conn.play(discord.FFmpegPCMAudio(file))

        # check every half second if the audio is done playing
        while conn.is_playing():
            if skip == False:
                await asyncio.sleep(0.5)


        conn.stop()
        await conn.disconnect()
        VC_LOCK.release()


async def skip():
    skip = True