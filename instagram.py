import requests, re, time, json
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

################################# Instagram Posts and Reels #########################################
def instaPost(url, firefox, button):
    if (auth(url, firefox, button) == True):   
        firefox.get(url)
        time.sleep(1)
        html = firefox.page_source
        time.sleep(1)
        encodedImg = re.search(r'"display_url":"(.*?)",', html)
        encodedVideo = re.search(r'"video_url":"(.*?)",', html)
        if (encodedImg == None and encodedVideo == None):
            return False
        else:
            if (encodedVideo == None):
                decoded = (encodedImg.group(1).replace(r"\u0026", "&"))
            else:
                decoded = (encodedVideo.group(1).replace(r"\u0026", "&"))
            return decoded
############################### Instagram Stories ########################################################
def instaStories(url, firefox, button):
    if (auth(url, firefox, button) == True):
        firefox.get(url)   
        time.sleep(5)
        view = firefox.find_element_by_class_name('sqdOP.L3NKy.y1rQx.cB_4K')
        view.click()
        time.sleep(1)
        img = ''
        video = ''
        if (bool (len(firefox.find_elements_by_tag_name('source'))) > 0):
            video = firefox.find_element_by_tag_name('source').get_attribute("src")
            return video
        else:
            img = firefox.find_element_by_tag_name("img").get_attribute("src")
            return img
        
          
########################### Authentication Method (Login) ####################################################
       
def auth(url, firefox, button):
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
                                 