import pytube
import glob
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram

load = u' \U0001f504'

def getYou(url, bot, chat_id):
    if os.path.isdir('/home/mateus/Documents/Python/telegram_bot/youtube') == False:
        os.mkdir('/home/mateus/Documents/Python/telegram_bot/youtube')
    path = '/home/mateus/Documents/Python/telegram_bot/youtube'
    yt = pytube.YouTube(url).streams.filter(res="720p").first().download(path)
    video = glob.glob(path  + '/*.mp4')
    final_path = ''
    ytPath = []
    for i in video:
        final_path = i
        size = os.path.getsize(i) / 1000000
        break
    if (size > 49.9999):
        video = VideoFileClip(str(final_path))
        duration = int(video.duration)
        start_time = 0
        end_time = 360
        parts = int(duration / 360)
        videopart = int(duration/360) + 1
        if (parts > (video.duration / 360)):
            parts = parts - 1
        if (duration <= 390):
            bot.send_message(chat_id=chat_id, text='Iniciando conversão...', timeout=60)
            subvideo = video.subclip(0, duration)
            bot.send_message(chat_id=chat_id, text='Finalizando...', timeout=60)
            subvideo.write_videofile('/home/mateus/Documents/Python/telegram_bot/youtube/youtube'  + '01' + '.mp4',  threads=8, logger=None, rewrite_audio=False, audio_codec='aac', preset = 'veryfast', fps=24, bitrate='860k')
            os.remove(path)
            ytPath = glob.glob('/home/mateus/Documents/Python/telegram_bot/youtube' + '/*.mp4')
            return ytPath
        elif (duration > 360):
            if (duration % 360 == 0):
                bot.send_message(chat_id=chat_id, text='Iniciando conversão...', timeout=60)
                c = 1
                for i in range (parts):
                    if(end_time > duration):
                        break
                    subvideo = video.subclip(start_time, end_time)
                    bot.send_message(chat_id=chat_id, text='Processando ' + 'parte ' + str(c) + '/' + str(videopart) + '' + load, timeout=60)
                    c += 1
                    subvideo.write_videofile('/home/mateus/Documents/Python/telegram_bot/youtube/youtube'  + '0' + str(i+1) + '.mp4', threads=8, logger=None, rewrite_audio=False, audio_codec='aac', preset = 'veryfast', fps=24, bitrate='860k')
                    start_time += 360.00
                    end_time += 360.00
            elif (duration % 360 > 0):
                bot.send_message(chat_id=chat_id, text='Iniciando conversão...', timeout=60)
                i = 0
                c = 1
                end_custom = (360 * parts) + (duration % 360)
                while i < parts:
                    subvideo = video.subclip(start_time, end_time)
                    bot.send_message(chat_id=chat_id, text='Processando ' + 'parte ' + str(c) + '/' + str(videopart) + '' + load, timeout=60)
                    subvideo.write_videofile('/home/mateus/Documents/Python/telegram_bot/youtube/youtube'  + '0' + str(i+1) + '.mp4', threads=8, logger=None, rewrite_audio=False, audio_codec='aac', preset = 'veryfast', fps=24, bitrate='860k')
                    c += 1
                    start_time += 360.00
                    end_time += 360.00
                    i += 1
                if (i == parts):
                    subvideo = video.subclip(start_time, end_custom)
                    bot.send_message(chat_id=chat_id, text='Processando ' + 'parte ' + str(c) + '/' + str(videopart) + '' + load, timeout=60)
                    subvideo.write_videofile('/home/mateus/Documents/Python/telegram_bot/youtube/youtube'  + '0' + str(i+1) + '.mp4', threads=8, logger=None, rewrite_audio=False, audio_codec='aac', preset = 'veryfast', fps=24, bitrate='860k')
                os.remove(final_path)
                ytPath = glob.glob('/home/mateus/Documents/Python/telegram_bot/youtube' + '/*.mp4')
                return ytPath
    else:
        return final_path
        '''
        os.remove(final_path)
        yt = pytube.YouTube(url).streams.filter(only_audio=True).first().download(path)
        video = glob.glob(path  + '/*.mp4')
        for i in video:
            final_path = i
            break
        clip = AudioFileClip(final_path)
        audio_path = final_path.replace('mp4', 'mp3')
        clip.write_audiofile(audio_path)
        os.remove(final_path)
        return audio_path'''
