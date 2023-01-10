'''
Utilities for interacting with voice channels
'''

import asyncio
import os
from . import queue
import discord

VC_LOCK = asyncio.Lock()

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

async def play(channel, name):
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
        queue.add_to_queue(name)
    else:
        print("playing")
        if name is not None:
            queue.add_to_queue(name)
        else:
            await queue.remove_from_queue(0)
        async with VC_LOCK:
            playing = True
            conn = await channel.connect()
            while playing:
                try:
                    conn = await channel.connect()
                except discord.errors.ClientException:
                    pass
                cur_file = ("sounds/" + queue.get_top() + ".mp3")
                # executable=("C:\Program Files (x86)\\ffmpeg-master-latest-win64-gpl\\bin"))
                source = await discord.FFmpegOpusAudio.from_probe(cur_file)
                conn.play(source)
                # check every half second if the audio is done playing
                while conn.is_playing():
                    await asyncio.sleep(0.5)
                conn.stop()
                await queue.remove_from_queue(0)
                if not queue.songs():
                    playing = False

            await conn.disconnect()



"""
Sunset'd join and play code.
Kept for research and reference

This Reference Code given by 
Rafi Bayer
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
