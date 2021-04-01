import pytube
import glob
import os


def getYou(url):
    os.mkdir('/home/mateus/Documents/Python/telegram_bot/youtube')
    path = '/home/mateus/Documents/Python/telegram_bot/youtube'
    yt = pytube.YouTube(url).streams.filter(only_audio=True).first().download(path)
    video = glob.glob(path  + '/*.mp4')
    return video
