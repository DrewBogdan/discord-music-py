import discord
from discord.ext import commands


class Responses(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot


    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('hello'):
            await message.channel.send('Hello?')