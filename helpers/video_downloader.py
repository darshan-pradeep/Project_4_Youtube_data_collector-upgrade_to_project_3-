import pytube
from io import BytesIO
import re


def get_download_stream(url):
        buffer = BytesIO()
        yt = pytube.YouTube(url)
        stream = yt.streams.get_by_itag(18)
        filesize = (stream.filesize / 1024)
        filename = re.sub(" ", "_", stream.default_filename)
        stream.stream_to_buffer(buffer)
        buffer.seek(0)
        return buffer, filename, filesize


def main(video_id):
    url='https://www.youtube.com/watch?v='+video_id
    buffer, filename, filesize = get_download_stream(url)
    return buffer,filename