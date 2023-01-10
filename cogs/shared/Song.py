from . import utils


class Song:

    title = ""
    url = ""

    def __init__(self, url, title):
        if url is None and title is None:
            print("error")
            self.title = "NA"
            self.url = "youtube.com"

        if title is None:
            self.title = utils.get_title(url)
            self.url = url
        elif url is None:
            self.url = utils.get_url(title)
            self.title = title
        else:
            self.url = url
            self.title = title


    def download_song(self):
        return None