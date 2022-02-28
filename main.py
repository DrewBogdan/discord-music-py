import discord
from discord import Client
from discord.ext.commands import Bot
from discord.ext import commands
from cogs import play_cog
from cogs import util_cog
from cogs import response_cog

class MusicBot(Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('hello'):
            await message.channel.send('Hello?')

if __name__ == '__main__':

    # your secret bot token
    token = open('token.txt').read()

    bot = MusicBot(command_prefix='!')

    bot.add_cog(play_cog.Play(bot))
    bot.add_cog(util_cog.Util(bot))

    print("bot starting up...")
    bot.run(token)