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
    if url.__contains__("playlist"):
        playlist_parse = url.split("playlist/")
        id_string = playlist_parse[1]
        id = id_string.split("?si=")[0]
        return id
    elif url.__contains__("track"):
        playlist_parse = url.split("track/")
        id_string = playlist_parse[1]
        id = id_string.split("?si=")[0]
        return id


async def get_tracks(id):
    id_string = 'spotify:playlist:' + id

    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.SPOTIFY_ID, client_secret=config.SPOTIFY_SECRET))

    res = spotify.playlist_items(id_string, limit=100)

    tracks = get_playlist_tracks(res, spotify)

    parsed_tracks = []
    for item in tracks:
        search_term = ""
        search_term += (item['track']['name']) + " "  # name of the track
        search_term += (item['track']['artists'][0]['name'])  # artist of the track
        parsed_tracks.append(search_term)
    return parsed_tracks


async def get_track(id):
    spotify = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(client_id=config.SPOTIFY_ID, client_secret=config.SPOTIFY_SECRET))
    track = spotify.track(id)
    search_term = ""
    search_term += (track['name']) + " "  # name of the track
    search_term += (track['artists'][0]['name'])  # artist of the track
    return search_term


async def play_song(url):
    id = await parser(url)
    track = await get_track(id)
    return track

async def play_playlist(url):
    id = await parser(url)
    tracks = await get_tracks(id)
    return tracks



def get_playlist_tracks(results, spotify):
    tracks = results['items']
    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])
    return tracks
