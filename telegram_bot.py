import requests, re, time, urllib, os, webbrowser, json, tempfile, shutil
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips

####################################### Twitter Video #####################################################
def getTwitter(url, firefox, bot, chat_id):
    temp_dir = tempfile.mkdtemp()
    directory_final = '/home/mateus/Documents/Python/telegram_bot'
    firefox.get(url)
    time.sleep(5)
    log = firefox.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")
    video =''
    path = ''
    with open(temp_dir + "/items.json", "w") as jsonFile:
        json.dump(log, jsonFile, indent = 6)
    jsonFile.close()
    with open (temp_dir + "/items.json", "r") as jsonFile:
        json_decoded = json.load(jsonFile)
        for i in range(len(json_decoded)):
            if (re.match(r'https://video.twimg.com/', json_decoded[i]['name']) != None):
                video = json_decoded[i]['name']
                break
    jsonFile.close()
    if (re.search(r'https://video.twimg.com/(.*?).m3u8', video) != None):
        m3u8c = re.search(r'https://video.twimg.com(.*?)?tag=', video)
        encoded = []
        if (m3u8c == None):
            tipo='m4s'
            urllib.request.urlretrieve(video, temp_dir + '/temp.txt')
            with open (temp_dir + "/temp.txt", "r") as tempF:
                for line in tempF:
                    if(re.search(r'.ts', line) != None):
                        encoded.append('https://video.twimg.com' + line)
                        tipo ='ts'
            tempF.close()
            collection =[]
            if(tipo == 'ts'):
                for i in range(len(encoded)):
                    name = temp_dir + '/temp' + '0' + str(i) + '.ts'
                    urllib.request.urlretrieve(encoded[i], name)
                    video = VideoFileClip(name)
                    collection.append(video)
                bot.send_message(chat_id=chat_id, text='Finalizando...', timeout=60)
                twitter = concatenate_videoclips(collection)
                final_name = 'twitter.mp4'
                twitter.to_videofile(directory_final + '/' + final_name, threads=8, logger=None, rewrite_audio=False, audio_codec='aac', preset = 'veryfast', fps=24)
                path = (directory_final + '/' + final_name)
                return path
            else:
                path = 'inválido'
                return path

        elif (m3u8c != None):
            tipo='m4s'
            urllib.request.urlretrieve(video, temp_dir + '/temp.txt')
            with open (temp_dir + "/temp.txt", "r") as tempF:
                for line in tempF:
                    if(re.search(r'.m3u8', line) != None):
                        m3u8c2 = 'https://video.twimg.com' + line
                        break
            tempF.close()
            urllib.request.urlretrieve(m3u8c2, temp_dir + '/temp.txt')
            with open (temp_dir + "/temp.txt", "r") as tempF:
                for line in tempF:
                    if(re.search(r'.ts', line) != None):
                        encoded.append('https://video.twimg.com' + line)
                        tipo = 'ts'
            tempF.close()
            collection =[]
            if (tipo == 'ts'):
                for i in range(len(encoded)):
                    name = temp_dir + '/temp' + '0' + str(i) + '.ts'
                    urllib.request.urlretrieve(encoded[i], name)
                    video = VideoFileClip(name)
                    collection.append(video)
                bot.send_message(chat_id=chat_id, text='Finalizando...', timeout=60)
                twitter = concatenate_videoclips(collection)
                final_name = 'twitter.mp4'
                twitter.to_videofile(directory_final + '/' + final_name, threads=8, logger=None, rewrite_audio=False, audio_codec='aac', preset = 'veryfast', fps=24)
                path = (directory_final + '/' + final_name)
                return path
            else:
                path = 'inválido'
                return path

        else:
            tipo='m4s'
            encoded = []
            with open (temp_dir + "/items.json", "r") as jsonFile:
                json_decoded = json.load(jsonFile)
                for i in range(len(json_decoded)):
                    if(re.search('"(.*?).ts', json_decoded[i]['name']) != None):
                        encoded.append(json_decoded[i]['name'])
                        tipo='ts'
            jsonFile.close()
            collection =[]
            if (tipo == 'ts'):
                for i in range(len(encoded)):
                    name = temp_dir + '/temp' + '0' + str(i) + '.ts'
                    urllib.request.urlretrieve(encoded[i], name)
                    video = VideoFileClip(name)
                    collection.append(video)
                bot.send_message(chat_id=chat_id, text='Finalizando...', timeout=60)
                twitter = concatenate_videoclips(collection)
                final_name = 'twitter.mp4'
                twitter.to_videofile(directory_final + '/' + final_name, threads=8, logger=None, rewrite_audio=False, audio_codec='aac', preset = 'veryfast', fps=24)
                path = directory_final + '/' + final_name
                return path
            else:
                path = 'inválido'
                return path
####################################################################################################
