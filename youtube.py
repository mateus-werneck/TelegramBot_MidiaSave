import os, time, glob, pytube, shutil, tempfile
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


load = u' \U0001f504'
runner = u' \U0001f3c3'

def getYou(url, bot, chat_id, formato):
    temp_dir = tempfile.mkdtemp()
    if (formato == '.mp4'):
        try:
            yt = pytube.YouTube(url).streams.filter(res="720p").first().download(temp_dir)
        except:
            yt = pytube.YouTube(url).streams.filter(res="360p").first().download(temp_dir)
        video = glob.glob(temp_dir  + '/*.mp4')
        final_path = ''
        ytPath = []
        for i in video:
            final_path = i
            size = os.path.getsize(i) / 1000000
            break
        if (size > 49.9999):
            video = VideoFileClip(final_path)
            duration = int(video.duration)
            start_time = 0
            end_time = 600
            parts = int(duration / 600)
            videopart = int(duration/ 600) + 1
            if (parts > (video.duration / 600)):
                parts = parts - 1
            if (duration <= 630):
                subvideo = video.subclip(0, duration)
                bot.send_message(chat_id=chat_id, text='Finalizando ' + runner, timeout=60)
                subvideo.write_videofile(temp_dir + '/youtube'  + '01' + '.mp4',  threads=8, logger=None, rewrite_audio=False, audio_codec='aac', preset = 'veryfast', fps=30, bitrate='520k')
                ytPath = temp_dir + '/youtube'  + '01' + '.mp4'
                bot.send_video(chat_id=chat_id, video = open(ytPath, 'rb'), timeout=3600)
                shutil.rmtree(temp_dir)
                return ytPath
            elif (duration > 630):
                if (duration % 600 == 0):
                    c = 1
                    for i in range (parts):
                        if(end_time > duration):
                            break
                        subvideo = video.subclip(start_time, end_time)
                        bot.send_message(chat_id=chat_id, text='Processando ' + 'parte ' + str(c) + '/' + str(videopart) + '' + load, timeout=60)
                        c += 1
                        subvideo.write_videofile(temp_dir + '/youtube'  + '0' + str(i+1) + '.mp4', threads=8, logger=None, rewrite_audio=False, audio_codec='aac', preset = 'veryfast', fps=30, bitrate='550k')
                        bot.send_video(chat_id=chat_id, video = open(temp_dir + '/youtube'  + '0' + str(i+1) + '.mp4', 'rb'), timeout=3600)
                        start_time += 600.00
                        end_time += 600.00
                elif (duration % 600 > 0):
                    i = 0
                    c = 1
                    end_custom = (600 * parts) + (duration % 600)
                    while i < parts:
                        subvideo = video.subclip(start_time, end_time)
                        bot.send_message(chat_id=chat_id, text='Processando ' + 'parte ' + str(c) + '/' + str(videopart) + '' + load, timeout=60)
                        subvideo.write_videofile(temp_dir + '/youtube'  + '0' + str(i+1) + '.mp4', threads=8, logger=None, rewrite_audio=False, audio_codec='aac', preset = 'veryfast', fps=30, bitrate='550k')
                        bot.send_video(chat_id=chat_id, video = open(temp_dir + '/youtube'  + '0' + str(i+1) + '.mp4', 'rb'), timeout=3600)
                        start_time += 600.00
                        end_time += 600.00
                        i += 1
                        c += 1
                    if (i == parts):
                        subvideo = video.subclip(start_time, end_custom)
                        bot.send_message(chat_id=chat_id, text='Processando ' + 'parte ' + str(c) + '/' + str(videopart) + '' + load, timeout=60)
                        subvideo.write_videofile(temp_dir + '/youtube'  + '0' + str(i+1) + '.mp4', threads=8, logger=None, rewrite_audio=False, audio_codec='aac', preset = 'veryfast', fps=30, bitrate='550k')
                        time.sleep(1)
                        bot.send_video(chat_id=chat_id, video = open(temp_dir + '/youtube'  + '0' + str(i+1) + '.mp4', 'rb'), timeout=3600)
                    ytPath = glob.glob(temp_dir + '/*.mp4')
                    shutil.rmtree(temp_dir)
                    return ytPath
        else:
            bot.send_video(chat_id=chat_id, video = open(final_path, 'rb'), timeout=3600)
            shutil.rmtree(temp_dir)
            return final_path
    elif formato == '.mp3':
        yt = pytube.YouTube(url).streams.filter(only_audio=True).first().download(temp_dir)
        video = glob.glob(temp_dir  + '/*.mp4')
        for i in video:
            final_path = i
            break
        clip = AudioFileClip(final_path)
        audio_path = final_path.replace('mp4', 'mp3')
        clip.write_audiofile(audio_path, logger=None)
        bot.send_audio(chat_id=chat_id, audio = open(audio_path, 'rb'), timeout=3600)
        shutil.rmtree(temp_dir)
        return final_path
