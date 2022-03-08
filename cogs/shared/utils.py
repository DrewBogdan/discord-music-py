import os
import re
import urllib
import yt_dlp
from . import queue


def get_url(content):
    search_keyword = ""
    parsed = content.split(" ")
    for string in parsed:
        if search_keyword == "":
            search_keyword += string
        else:
            search_keyword += "_" + string
    try:
        url = "https://www.youtube.com/results?search_query=" + search_keyword
        info = urllib.request.urlopen(url)
        video_ids = re.findall(r"watch\?v=(\S{11})", info.read().decode())
        if len(video_ids) > 0:
            return "https://www.youtube.com/watch?v=" + video_ids[0]
    except UnicodeEncodeError:
        pass


def download(url, print_message=True):
    # the idea of this part is to download them once
    # they are added to the queue so when it runs into the main
    # play function its quicker
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': f"sounds" + '/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info).split("\\")[1]
        name = file.split(".webm")[0]
        return f"sounds/" + name + ".mp3"


def get_title(url):
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        name = info.get('title', None)
        return name


def background_download(track):
    for x in range(len(track)):
        file = f"sounds/{track[x]}.mp3"
        if not os.path.exists(file):
            url = get_url(track[x])
            if url is not None:
                filename = download(url, False)
                queue.queue[x+1] = (os.path.splitext(filename)[0]).split("sounds/")[1]


def add_urls(tracks):
    for val in tracks:
        url = get_url(val)
        if url is not None:
            title = get_title(url)
            queue.add_to_queue(title)