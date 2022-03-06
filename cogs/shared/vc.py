'''
Utilities for interacting with voice channels
'''

import asyncio
import os
from . import queue
import discord

VC_LOCK = asyncio.Lock()
Skip = False


async def play(channel, file):
    """
    Connects to the given voice channel, playing the given .mp3 file
    over voice, before disconnecting

    Args:
        channel (VoiceChannel): Voice Channel to connect to
        file (str): path to .mp3 file to play
    """
    print("added")
    if queue.songs():
        print("queueing")
        await queue.add_to_queue(file)
    else:
        print("playing")
        await queue.add_to_queue(file)
        async with VC_LOCK:
            playing = True
            conn = await channel.connect()
            while playing:
                cur_file = queue.get_top()
                # executable=("C:\Program Files (x86)\\ffmpeg-master-latest-win64-gpl\\bin"))
                conn.play(discord.FFmpegPCMAudio(cur_file))
                # check every half second if the audio is done playing
                while conn.is_playing() and not await skipped():
                    await asyncio.sleep(0.5)
                Skip = False
                conn.stop()
                await queue.remove_from_queue(0)
                if not queue.songs():
                    playing = False

            await conn.disconnect()


async def skipped():
    return Skip


async def skip():
    Skip = True


"""
Sunset'd join and play code.
Kept for research and reference
"""


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
            await asyncio.sleep(0.5)

        conn.stop()
        await conn.disconnect()
