import random
import string
from .shared import vc, utils
import discord
from discord.ext import commands

class Responses(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.__contains__('<@!943706887545815071>'):
            await message.delete()
        if message.content.lower().__contains__('hello'):
            await message.channel.send('Hello?')
        if message.content.lower().startswith('hey'):
            hey = 'he'
            rand = random.randint(1,100)
            for x in range(rand):
                hey += 'y'
            await message.channel.send(hey)
        if message.content.lower().__contains__('fuck off'):
            await message.channel.send('How about no?')
        elif message.content.lower().__contains__('fuck you'):
            await message.channel.send('Fuck you!')
        elif message.content.lower().__contains__('fuck'):
            await message.channel.send('me?')

        if message.content.lower().__contains__('gn'):
            await message.channel.send('gn honey bunches :heart_eyes:')
        if message.content.lower().startswith('call me daddy'):
            await message.channel.send('daddy :tired_face:')

        if message.content.lower().startswith('?'):
            rand = random.randint(0, 100)
            if rand <= 20:
                await message.channel.send('?')
            if 20 < rand <= 60:
                await message.channel.send('Read the chat dumbass')
            if 60 < rand < 100:
                await message.channel.send('Are you blind?')
            if rand == 100:
                await message.channel.send('You are a coward, and history will forget you')
        if message.content.lower().__contains__('wucka') or message.content.lower().__contains__('woka'):
            rand = random.randint(0,101)
            if rand < 20:
                await message.channel.send('What.')
            if 20 <= rand < 40:
                await message.channel.send('I\'m trying to sleep')
            if 40 <= rand < 60:
                await message.channel.send('dad told me not to talk to strangers')
            if 60 <= rand < 70:
                await message.channel.send('https://tenor.com/bzuiW.gif')
            if 70 <= rand < 80:
                await message.channel.send('If only I wasn\'t trapped in a basement...')
            if 80 <= rand < 90:
                await message.channel.send('I\'m busy with your mom, give me a sec')
            if 90 <= rand < 100:
                await message.channel.send(':|')
                await vc.play(message.author.voice.channel, "sounds/ugly.mp3")
            if rand == 100:
                await message.channel.send('YOU DARE SUMMON ME?')
            if rand == 101:
                await message.channel.send('https://cdn.discordapp.com/attachments/420073745651335188/948279662755323974/unknown.png')
                await message.channel.send('This is how I feel about you.')
        if message.content.lower().startswith('yeah you'):
            await message.channel.send(':(')
        if message.content.lower().__contains__('uninstall'):
            await message.channel.send('I gotta uninstall my dick from your mom first')
        if message.content.lower().__contains__('creeper'):
            await vc.play(message.author.voice.channel, "sounds/creeper.mp3")

