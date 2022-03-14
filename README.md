# Discord Music Bot
By Drew Bogdan

## Goal
The Goal of this project was to create a bot that can play music in a discord voice channel from multiple sources
The reason for this was that alot of the current music bots got shutdown, so I wanted to create a bot that performed
the same actions for me and my friends. 

## What I learned


### API's

The main thing this project taught me was how to use a variety of API's, and what to look for in the documentation
to get what you want out of the API.

I used 3 different api's in this project:
* Spotipy - A spotify API that works with python, and allowed me to get the song lists of playlist links given to the bot.
* Youtube-DL - This API is what allowed me to download songs off of youtube with the given link.
* Discord.py - This is a python interpretation of the discord API, and allowed the bot to communicate with discord.

### Multithreading and Asynronization 

Another big step in learning that i took in this project was understanding multithreading and async functionality.
The main use of asyncfunctionality came in the way the locks worked, and how the voice function was locked when one
song was being played, and i originally used that to create a semblance of a queue, but now my queue system uses 
locks for when people are removing from it to stop 2 things from being removed at once from the queue. This took some time
to understand, but once i got the hang of it i understood how it worked. Also the discord API requires all the functions
that explain commands to be async to allowed them to be called at any time when the command is run, so i understood how that worked
and why it needed to be done from that. 

Multi-threading became a big issue that i needed to tackle when it came to adding the spotify playlists to the queue.
I had to figure out how to get the thread to download in the background so as not to interuppt the current play of the bot.
I was able to figure that out though, and i made multiple processes background thread processes to speed up other parts of the bot.

## What the bot does
Currently the bot's main function is to play music. It does this in a variety of ways. 
* One way it does this is if I add in a mp3 file to the sounds folder, It will play it when i run a command and give the files name, 
* Another way, is you can give the bot a youtube link, and it will download the song and play the mp3. 
* You can also just type the name of a song and it will read the name, search for it on youtube, get the top result, then download it and play it
* Lastly, the bot can take a spotify playlist link, and read all the songs and their respective artists and search for them on youtube. From this it will add all the song names to the queue and have them ready to play

The bot has a queue functionality with it aswel that is built to handle any number of songs being played at once. It does
this by queuing up the names for songs, then as the queue is being walked through, the top 3 songs of the queue are being
checked constantly if they are downloaded, if not it will download them on a seperate thread, and it will then play the song when its turn is up
and delete the file immediately after finishing the play of the song, That way the folder doesnt fill up with hundreds of downloaded 
songs. 

## Issues

This bot went through many different iterations of how it should and how it did function.
Originally i just planned to have it play links one at a time, and i relied on lock's and
the request for the locked function to hold a "queue"

Then, I decided to add in the search function so that a link was not required each time. This
took a bit of work because of youtube and their link structure. 

Once i figured that out, I decided that I should not just settle for that so i begun reworking the
queue system so that a queue could be printed, manipulated, and changed during the play of an earlier song.

With this new and improved queue system, I was able to finally add in the spotify playlist functionality, but this
brought in a whole new slew of issues, the main one being, if a playlist of 200 songs was too be played, my code 
originally had to download all 200 songs before starting the play of the first song in the playlist. I redid this by 
reworking the queue system again to only download the top 3 songs of the queue, and as one song got removed, the next song in the queue was downloaded.
I chose 3 because that gives enough buffer time that if someone wants to skip 4 songs, by the time they get to the 4th the next 3 in the queue are 
downloaded.

## Future plans

This bot, while very fun to make, and very functional at its current state, has alot of quality of life to update in it.
The main thing i want to work on is making skip better, adding in a stop command, and adding in a pause command. These
things are actually pretty tough with how the code is currently setup, so i would have to rework the entire way that 
the bot plays sounds into the voice channel, But it is at the top of my list currently because it will make the bot even better
and allow me and my friends to have alot more fun with it

Another plan i have is to add in more chat functions, and hopefully create a very basic descision tree and give the bot
a slight amount of intelligence to have a basic conversation with people, wheather that be hello and good bye, or some discussion
about the weather.

## Acknowledgments

At the start of this process I was given guidance and starter code from
**Rafi Bayer** that helped me figure out things along the way. This code allowed
the bot to play mp3's that i put in the sound folder myself, and ran the command
for. 

At this point Almost none of that refrence code exists in the program anymore,
Where the remaining refrence code can be found is in main.py, the set up of the bot
was given to me and there was no need to change it at the current build of the bot.
but all of the refrence doe was a big help in helping me understand how the 
discord API works, and where to start from.
