import re
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from twitter import getTwitter
from instagram import instaPost, instaStories, instaTV
from youtube import getYou
##################################### Open Firefox #########################################
firefox_options = Options()
firefox_options.add_argument("--headless")
firefox = webdriver.Firefox(options=firefox_options)
firefox.set_page_load_timeout(60)
#################################### Process Media Type and Get Media #######################
def getMedia(url, button, bot, chat_id, formato):
     url = url
     igtv = re.search('/tv/', url)
     stories = re.search('/stories/', url)
     posts = re.search('/p/', url)
     reel = re.search ('/reel/', url)
     igtv = re.search('/tv/', url)
     twt = re.search('twitter.com/', url)
     twt2 = re.search('t.co', url)
     yt = re.search('youtube', url)
     yt2 = re.search('youtu.be', url)
################### Posts and Reels Instagram #######################################

     if (posts != None or reel != None):
        source = instaPost(url, firefox, button, bot, chat_id)
        if re.search('instagram', source) != None or re.search("IGTV", source) != None:
            return source
        else:
            source = ''
            return source

################## Instagram Stories ################################################

     elif(stories != None):
        source = instaStories(url, firefox, button, bot, chat_id)
        if re.search('instagram', source) != None:
            return source
        else:
            source = ''
            return source

#################### IGTV ###############################################################
     elif(igtv != None):
        source = instaTV(url, firefox, button, bot, chat_id)
        if type(source) is list:
            for i in source:
                if (re.search('IGTV', i) != None):
                    return source
        elif type(source) is str:
            if re.search('.mp4', source) != None:
                return source
        else:
            source = ''
            return source

 ################ Twitter Videos ########################################################

     elif twt != None or twt2 != None:
        path = ''
        path = getTwitter(url, firefox, bot, chat_id)
        return path

################ Youtube Audio ##########################################################

     elif yt != None or yt2 != None:
        path = ''
        path = getYou(url, bot, chat_id, formato)
        return path
