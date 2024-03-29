'''
Utilities for interacting with the queue
'''

import asyncio
import os
import random
import threading

from . import utils, Song

import discord

Q_LOCK = asyncio.Lock()
queue = []


def add_to_queue(song):
    #async with Q_LOCK:
    if len(queue) < 2:
        queue.append(song)

        if type(song) != str and song.url is not None:
            print(song.url)
            file = utils.download(song.url)
            if len(queue) == 1:
                queue[0] = song
            else:
                queue[1] = song
    else:
        queue.append(song)


async def remove_from_queue(index):
    async with Q_LOCK:
        if type(queue[index]) == str:
            val = queue[index]
        else:
            val = queue[index].title
        queue.remove(queue[index])
        if val != "minecraft" and val != "music" and val != "creeper" and val != "ugly":
            try:
                os.remove(f"sounds/{val}.mp3")
            except FileNotFoundError:
                pass
        return val


def songs():
    if len(queue) == 0:
        return False
    return True


def get_top():
    """
    Only time this gets called is when it is playing in vc
    """
    if songs():
        if len(queue) < 4:
            download_queue = []
            for x in range(len(queue)):
                if x != 0:
                    download_queue.append(queue[x])
            download_thread = threading.Thread(target=utils.background_download, name="Downloader", args=(download_queue,))
            download_thread.start()
        else:
            download_thread_stag = threading.Thread(target=utils.background_download, name="Downloader", args=([queue[1], queue[2], queue[3]],))
            download_thread_stag.start()

        if type(queue[0]) == str:
            return queue[0]
        return queue[0].title
    return None


async def print_queue(ctx):
    async with Q_LOCK:
        message = ""
        for x in range(len(queue)):
            if x == 0:
                # (os.path.splitext(queue[x])[0]).split("sounds/")[1] Old style of queue
                if type(queue[x]) == str:
                    message += ("**Current Song:** " + queue[x] + "\n")
                else:
                    message += ("**Current Song:** " + queue[x].title + "\n")
            else:
                if type(queue[x]) == str:
                    message += ("**" + str(x) + "**" + ": " + queue[x] + "\n")
                else:
                    message += ("**" + str(x) + "**" + ": " + queue[x].title + "\n")
            if x % 10 == 0 and x != 0:
                await ctx.send(message)
                message = ""
        await ctx.send(message)


async def clear_queue():
    async with Q_LOCK:
        queue.clear()


async def shuffle():
    async with Q_LOCK:
        temp = queue[0]
        queue.remove(queue[0])
        random.shuffle(queue)
        queue.insert(0, temp)
        if len(queue) < 4:
            download_queue = []
            for x in range(len(queue)):
                if x != 0:
                    download_queue.append(queue[x])
            download_thread = threading.Thread(target=utils.background_download, name="Downloader", args=(download_queue,))
        else:
            download_thread = threading.Thread(target=utils.background_download, name="Downloader", args=([queue[1], queue[2], queue[3]],))
        download_thread.start()

