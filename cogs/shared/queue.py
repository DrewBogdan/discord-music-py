'''
Utilities for interacting with the queue
'''

import asyncio
import os
import random
import threading

from . import utils

import discord

Q_LOCK = asyncio.Lock()
queue = []


def add_to_queue(name):
    #async with Q_LOCK:
    if len(queue) < 2:
        queue.append(name)
        if "http" not in name:
            url = utils.get_url(name)
        else:
            url = name

        if url is not None:
            file = utils.download(url)
            if len(queue) == 1:
                queue[0] = (os.path.splitext(file)[0]).split("sounds/")[1]
            else:
                queue[1] = (os.path.splitext(file)[0]).split("sounds/")[1]
    else:
        queue.append(name)


async def remove_from_queue(index):
    async with Q_LOCK:
        val = queue[index]
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

        return queue[0]
    return None


async def print_queue(ctx):
    async with Q_LOCK:
        message = ""
        for x in range(len(queue)):
            if x == 0:
                # (os.path.splitext(queue[x])[0]).split("sounds/")[1] Old style of queue
                message += ("**Current Song:** " + queue[x] + "\n")
            else:
                message += ("**" + str(x) + "**" + ": " + queue[x] + "\n")
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

