import requests, re, time, json, os, urllib, glob
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from moviepy.video.io.VideoFileClip import VideoFileClip
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram

load = u' \U0001f504'
################################# Instagram Posts and Reels #########################################
def instaPost(url, firefox, button, bot, chat_id):
    if (auth(url, firefox, button, bot) == True):
        firefox.get(url)
        time.sleep(1)
        '''
        IGTV = firefox.find_elements_by_xpath('.//span[@class = "PJXu4"]')
        if (IGTV[1].text == 'IGTV'):
            instaTV(url, firefox, button)'''
        #else:
        html = firefox.page_source
        time.sleep(1)
        encodedImg = re.search(r'"display_url":"(.*?)",', html)
        encodedVideo = re.search(r'"video_url":"(.*?)",', html)
        if (encodedImg == None and encodedVideo == None):
            decoded = ''
            return decoded
        else:
            bot.send_message(chat_id=chat_id, text='Finalizando...', timeout=60)
            if (encodedVideo == None):
                decoded = (encodedImg.group(1).replace(r"\u0026", "&"))
            else:
                decoded = (encodedVideo.group(1).replace(r"\u0026", "&"))
            return decoded
############################### Instagram Stories ########################################################
def instaStories(url, firefox, button, bot, chat_id):
    if (auth(url, firefox, button, bot) == True):
        firefox.get(url)
        time.sleep(5)
        view = firefox.find_element_by_class_name('sqdOP.L3NKy.y1rQx.cB_4K')
        view.click()
        time.sleep(1)
        img = ''
        video = ''
        if (bool (len(firefox.find_elements_by_tag_name('source'))) > 0):
            video = firefox.find_element_by_tag_name('source').get_attribute("src")
            bot.send_message(chat_id=chat_id, text='Finalizando...', timeout=60)
            return video
        elif (bool (len(firefox.find_elements_by_tag_name('source'))) == 0):
            img = firefox.find_element_by_tag_name("img").get_attribute("src")
            bot.send_message(chat_id=chat_id, text='Finalizando...', timeout=60)
            return img
        else:
            source = ''
            return source

def instaTV(url, firefox, button, bot, chat_id):
    bot.send_message(chat_id=chat_id, text='Isso pode demorar um pouco', timeout=60)
    if (auth(url, firefox, button, bot) == True):
        firefox.get(url)
        time.sleep(1)
        html = firefox.page_source
        time.sleep(1)
        encodedVideo = re.search(r'"video_url":"(.*?)",', html)
        if (encodedVideo == None):
            decoded = ''
            return decoded
        else:
            if os.path.isdir('/home/mateus/Documents/Python/telegram_bot/IGTV') == False:
                os.mkdir('/home/mateus/Documents/Python/telegram_bot/IGTV')
            if (encodedVideo != None):
                path = '/home/mateus/Documents/Python/telegram_bot/IGTV/IGTV.mp4'
                decoded = (encodedVideo.group(1).replace(r"\u0026", "&"))
                urllib.request.urlretrieve(decoded, path)
                size = os.path.getsize(path) / 1000000
                if size <= 49.9999:
                    return path
                else:
                    video = VideoFileClip(path)
                    duration = int(video.duration)
                    start_time = 0
                    end_time = 360
                    parts = int(duration / 360)
                    videopart = int(duration/360) + 1
                    end_custom = (360 * parts) + (duration % 360)
                    igtvPath = []
                    if (parts > (video.duration / 360)):
                        parts = parts - 1
                    if (duration <= 390):
                        bot.send_message(chat_id=chat_id, text='Iniciando conversão...', timeout=60)
                        subvideo = video.subclip(0, duration)
                        subvideo.write_videofile('/home/mateus/Documents/Python/telegram_bot/IGTV/IGTV'  + '01' + '.mp4', threads=8, preset="veryfast", logger=None, audio_codec='aac', rewrite_audio=False, fps=24, bitrate='860k')
                        bot.send_message(chat_id=chat_id, text='Finalizando...', timeout=60)
                        os.remove(path)
                        igtvPath = glob.glob('/home/mateus/Documents/Python/telegram_bot/IGTV' + '/*.mp4')
                        return igtvPath
                    else:
                        if (duration % 360 == 0):
                            bot.send_message(chat_id=chat_id, text='Iniciando conversão...', timeout=60)
                            c = 1
                            for i in range (parts):
                                if(end_time > duration):
                                    break
                                subvideo = video.subclip(start_time, end_time)
                                bot.send_message(chat_id=chat_id, text='Processando ' + 'parte ' + str(c) + '/' + str(videopart) + '' + load, timeout=60)
                                subvideo.write_videofile('/home/mateus/Documents/Python/telegram_bot/IGTV/IGTV'  + '0' + str(i+1) + '.mp4', threads=8, preset="veryfast", logger=None, audio_codec='aac', rewrite_audio=False, fps=24, bitrate='860k')
                                c +=1
                                start_time += 360.00
                                end_time += 360.00
                        elif (duration % 360 > 0):
                            bot.send_message(chat_id=chat_id, text='Iniciando conversão...', timeout=60)
                            i = 0
                            c = 1
                            while i < parts:
                                subvideo = video.subclip(start_time, end_time)
                                bot.send_message(chat_id=chat_id, text='Processando ' + 'parte ' + str(c) + '/' + str(videopart) + '' + load, timeout=60)
                                subvideo.write_videofile('/home/mateus/Documents/Python/telegram_bot/IGTV/IGTV'  + '0' + str(i+1) + '.mp4', threads=8, preset="veryfast", logger=None, audio_codec='aac', rewrite_audio=False, fps=24, bitrate='860k')
                                c +=1
                                start_time += 360.00
                                end_time += 360.00
                                i += 1
                            if (i == parts):
                                subvideo = video.subclip(start_time, end_custom)
                                bot.send_message(chat_id=chat_id, text='Processando ' + 'parte ' + str(c) + '/' + str(videopart) + '' + load, timeout=60)
                                subvideo.write_videofile('/home/mateus/Documents/Python/telegram_bot/IGTV/IGTV'  + '0' + str(i+1) + '.mp4', threads=8, preset="veryfast", logger=None, audio_codec='aac', rewrite_audio=False, fps=24, bitrate='860k')
                            os.remove(path)
                            igtvPath = glob.glob('/home/mateus/Documents/Python/telegram_bot/IGTV' + '/*.mp4')
                            return igtvPath
            else:
                decoded = ''
                return decoded
########################### Authentication Method (Login) ####################################################

def auth(url, firefox, button, bot):
    if (button == 0):
        username = 'pythonauthusr12345'
        password = 'instagramauthpass123'
        firefox.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        usern = firefox.find_element_by_name("username")
        usern.send_keys(username)
        passw = firefox.find_element_by_name("password")
        passw.send_keys(password)
        time.sleep(3)
        log_cl = firefox.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
        log_cl.click()
        time.sleep(4)
        title = firefox.title
        if (title == "Login • Instagram"):
            time.sleep(1)
            username = 'pythonauthusr1234'
            usern = firefox.find_element_by_name("username")
            usern.send_keys(username)
            passw = firefox.find_element_by_name("password")
            passw.send_keys(password)
            time.sleep(3)
            log_cl = firefox.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
            log_cl.click()
            time.sleep(4)
            title = firefox.title
            if (title == "Login • Instagram"):
                time.sleep(1)
                username = 'pythonauthusr123456'
                usern = firefox.find_element_by_name("username")
                usern.send_keys(username)
                passw = firefox.find_element_by_name("password")
                passw.send_keys(password)
                time.sleep(1)
                log_cl = firefox.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
                log_cl.click()
                time.sleep(4)
                title = firefox.title
                if (title == "Login • Instagram"):
                    firefox.quit()
                    return False
            else:
                return True

        else:
            return True
    elif(button > 0):
        title = firefox.title
        if (title != "Login • Instagram"):
            return True
        else:
            username = 'pythonauthusr12345'
            password = 'instagramauthpass123'
            firefox.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            usern = firefox.find_element_by_name("username")
            usern.send_keys(username)
            passw = firefox.find_element_by_name("password")
            passw.send_keys(password)
            time.sleep(3)
            log_cl = firefox.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
            log_cl.click()
            time.sleep(4)
            title = firefox.title
            if (title == "Login • Instagram"):
                time.sleep(1)
                username = 'pythonauthusr1234'
                usern = firefox.find_element_by_name("username")
                usern.send_keys(username)
                passw = firefox.find_element_by_name("password")
                passw.send_keys(password)
                time.sleep(3)
                log_cl = firefox.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
                log_cl.click()
                time.sleep(4)
                title = firefox.title
                if (title == "Login • Instagram"):
                    time.sleep(1)
                    username = 'pythonauthusr123456'
                    usern = firefox.find_element_by_name("username")
                    usern.send_keys(username)
                    passw = firefox.find_element_by_name("password")
                    passw.send_keys(password)
                    time.sleep(1)
                    log_cl = firefox.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
                    log_cl.click()
                    time.sleep(4)
                    title = firefox.title
                    if (title == "Login • Instagram"):
                        firefox.quit()
                        return False
