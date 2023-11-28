from pytube import YouTube
import time
from os import startfile,remove
from pymediainfo import MediaInfo

def get_length(filename):
    clip_info = MediaInfo.parse(filename)
    return clip_info.tracks[0].duration

vid = YouTube("https://www.youtube.com/watch?v=nbv84ixqiio")
downloaded = vid.streams.filter(progressive=True,file_extension="mp4").order_by("resolution").desc().first().download()
startfile(downloaded)
print(get_length(vid.title+".mp4"))
time.sleep(10)
remove(downloaded)