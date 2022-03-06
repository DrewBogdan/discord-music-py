'''
Utilities for playing spotify playlists
'''

import asyncio
import os
import queue
import spotipy
from . import config, utils, vc
from spotipy.oauth2 import SpotifyClientCredentials


async def parser(url):
    playlist_parse = url.split("playlist/")
    id_string = playlist_parse[1]
    id = id_string.split("?si=")[0]
    return id


async def get_tracks(id):
    id_string = 'spotify:playlist:' + id

    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.SPOTIFY_ID, client_secret=config.SPOTIFY_SECRET))

    tracks = spotify.playlist_items(id_string)

    parsed_tracks = []
    for i, item in enumerate(tracks['items']):
        search_term = ""
        search_term += (item['track']['name']) + " "  # name of the track
        search_term += (item['track']['artists'][0]['name'])  # artist of the track
        parsed_tracks.append(search_term)
    return parsed_tracks


async def play_playlist(url):
    id = await parser(url)
    tracks = await get_tracks(id)
    return tracks
