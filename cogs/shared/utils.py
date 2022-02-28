import re
import yt_dlp


async def get_url(content):

    regex = re.compile(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    if re.search(regex, content):
        result = regex.search(content)
        url = result.group(0)
        print(url)
        return url
    else:
        return None


async def download(url, ctx):
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
        await ctx.send("Queuing " + name)
        return f"sounds/" + name + ".mp3"