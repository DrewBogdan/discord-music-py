'''
Utilities for interacting with the queue
'''

import asyncio
import os

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
        return val


async def songs():
    async with Q_LOCK:
        if len(queue) == 0:
            return False
        return True


async def print_queue(ctx):
    async with Q_LOCK:
        message = ""
        for x in range(len(queue)):
            message += ("**" + str(x) + "**" + ": " + queue[x]) + "\n"
        await ctx.send(message)
