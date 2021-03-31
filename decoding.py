import re
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from twitter import getTwitter
from instagram import instaPost, instaStories
##################################### Open Firefox #########################################
firefox_options = Options()
firefox_options.add_argument("--headless")
firefox = webdriver.Firefox(options=firefox_options)
firefox.set_page_load_timeout(60)
#################################### Process Media Type and Get Media #######################
def getMedia(url, button):
     url = url
     stories = re.search('/stories/', url)
     posts = re.search('/p/', url)
     reel = re.search ('/reel/', url)
     twt = re.search('https://twitter.com/', url)
################### Posts and Reels Instagram #######################################
     if (posts != None or reel != None):
        source = instaPost(url, firefox, button)
        return source

################## Instagram Stories ################################################
     elif(stories != None):
        source = instaStories(url, firefox, button)
        return source

 ################ Twitter Videos ########################################################    
     elif(twt != None):
        path = ''
        path = getTwitter(url, firefox)
        return path
   

