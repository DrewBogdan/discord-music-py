'''
Utilities for interacting with the queue
'''

import asyncio
import os
import random

import discord

Q_LOCK = asyncio.Lock()
queue = []


async def add_to_queue(file):
    async with Q_LOCK:
        queue.append(file)


async def remove_from_queue(index):
    async with Q_LOCK:
        val = queue[index]
        queue.remove(queue[index])
        if val != "sounds/minecraft.mp3" and val != "sounds/music.mp3" and val != "sounds/creeper.mp3" and val != "sounds/ugly.mp3":
            os.remove(val)
        return (os.path.splitext(val)[0]).split("sounds/")[1]


def songs():
    if len(queue) == 0:
        return False
    return True


def get_top():
    if songs():
        return queue[0]
    return None


async def print_queue(ctx):
    async with Q_LOCK:
        message = ""
        for x in range(len(queue)):
            if x == 0:
                message += ("**Current Song:** " + (os.path.splitext(queue[x])[0]).split("sounds/")[1] + "\n")
            else:
                message += ("**" + str(x) + "**" + ": " + (os.path.splitext(queue[x])[0]).split("sounds/")[1] + "\n")
            if x % 10 == 0 and x != 0:
                await ctx.send(message)
                message = ""
        await ctx.send(message)


async def clear_queue():
    async with Q_LOCK:
        for val in queue:
            queue.remove(val)
            if val != "sounds/minecraft.mp3" and val != "sounds/music.mp3" and val != "sounds/creeper.mp3" and val != "sounds/ugly.mp3":
                os.remove(val)


async def shuffle():
    async with Q_LOCK:
        temp = queue[0]
        queue.remove(queue[0])
        random.shuffle(queue)
        queue.insert(0, temp)

