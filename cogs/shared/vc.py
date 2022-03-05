'''
Utilities for interacting with voice channels
'''

import asyncio
import os
import queue
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
            await asyncio.sleep(0.5)

        conn.stop()
        await conn.disconnect()



### TESTING PLAY WITH QUEUE ###
async def play(channel, file):
    """
    Connects to the given voice channel, playing the given .mp3 file
    over voice, before disconnecting

    Args:
        channel (VoiceChannel): Voice Channel to connect to
        file (str): path to .mp3 file to play
    """
    await queue.add_to_queue(file)
    if queue.songs():
        await queue.add_to_queue(file)
    else:
        async with VC_LOCK:
            playing = True
            cur_file = None
            while playing:
                conn = await channel.connect()
                # executable=("C:\Program Files (x86)\\ffmpeg-master-latest-win64-gpl\\bin"))
                if cur_file is None:
                    conn.play(discord.FFmpegPCMAudio(file))
                else:
                    conn.play(discord.FFmpegPCMAudio(cur_file))
                # check every half second if the audio is done playing
                while conn.is_playing():
                    await asyncio.sleep(0.5)
                conn.stop()
                cur_file = queue.remove_from_queue(0)
            await conn.disconnect()