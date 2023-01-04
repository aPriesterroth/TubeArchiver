from pytube import Playlist
from datetime import datetime

import hashlib
import zipfile
import os

url_playlist = 'PLAYLIST_URL_HERE';

path_log_videos = '../logs/log_videos.txt'
path_data = '../data/'

videos = []

def list_write():
    with open(path_log_videos, 'w') as file:
        for video in videos:
            file.write(str(video) + '\n')

def list_read():
    with open(path_log_videos, 'r') as file:
        return [line.rstrip('\n') for line in file]

def zip_video():
    dir = os.fsencode(path_data)
    for file in os.listdir(dir):
        file_name = os.fsdecode(file)
        print(file_name)
        if '.zip' not in file_name:
            file_zip = zipfile.ZipFile(file_name + '.zip', 'w')
            try:
                file_zip.write(file_name)
            finally:
                file_zip.close()
            os.remove(file)

videos = list_read()

playlist = Playlist(url_playlist);

for video in playlist.videos:
    v_title = video.title
    v_title_hash = hashlib.md5(v_title.encode()).hexdigest()

    if v_title_hash not in videos:
        print(datetime.now(), 'Downloading: ', v_title.encode('utf-8'))
        video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
        videos.append(hashlib.md5(video.title.encode()).hexdigest())
        #zip_video()

list_write()
