import os
import sys
import platform
import time
import traceback
import json
from fbchat import Client
from fbchat.models import *
import wget
from getpass import getpass
import os.path
import requests

if os.name == 'nt':
    path = str(os.environ["HOMEPATH"]) + "\\Desktop\\MessIm"
elif os.name == "posix":
    if os.path.exists("/storage/emulated/0"):
        try:
            os.mkdir('/storage/emulated/0/MessIm')
        except:
            pass
        path = "/storage/emulated/0/MessIm"
    elif platform.system() == 'Linux':
        path = os.path.expanduser("~/Desktop")
        if os.path.exists(path) == False:
            path = input('\nEnter the full path of folder for saving images: ')
            if path == '':
                path = os.path.dirname(os.path.realpath(__file__))
                os.chdir(path)
                os.mkdir('MessIm')
                path = path + "/MessIm"
    else:
        print("OS not detected.\nEnter the full path of folder for saving images: ")
        if path == '':
            path = os.path.dirname(os.path.realpath(__file__))
            os.chdir(path)
            os.mkdir('MessIm')
            path = path + "/MessIm"
                

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
print(os.path.basename(__file__))

ua_file_path = dir_path + "/ua.txt"

print("##################################\nMessenger Image Bulk Downloader\n##################################\n")
print("Not only images, you can also download GIFs and Videos from Messenger by reacting to messages, forwarding to your own conversation or just simply save all whoever sends you something.")
print("Images, GIFs and Videos will be saved at " + path + " directory in Desktop.\n")
option = int(input("Select an option:\n1) Save all images in one folder.\n2) Save images conversation name-wise.\n3) Save images conversation name-wise and time-wise.\n\nYour Choice: "))


if os.path.exists(ua_file_path) == False:
    words = "\n\nPlease enter the user agent of the browser you usually login to facebook. If you usually use Facebook App or Messenger App, then just use the browser's user agent.\n\n Just goto https://www.whatsmyua.info/, copy the text, paste here and press enter.\n\nYour browser\'s user agent will be something like this:\nMozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36\n\nUser agent is needed to fake this program as a normal browser you use, so that your account remains human-like to Facebook. You\'ll not have to enter the user agent every time you use this program. :-)"
    for char in words:
        time.sleep(0.01)
        sys.stdout.write(char)
        sys.stdout.flush()
        
    user_agent = input('\n\nUser agent: ')
    with open(ua_file_path, "w") as ua:
        ua.write(user_agent)
else:
    with open(ua_file_path, 'r') as ua:
        user_agent = ua.read().replace('\n', '')

       
count = 0

def download(option, url, threadname, time):
    global path
    try:
        os.mkdir(path)
    except:
        pass

    if option == 1:
        os.chdir(path)
        wget.download(url)
    elif option == 2:
        os.chdir(path)
        try:
            os.mkdir(threadname)
        except:
            pass
        os.chdir(threadname)
        wget.download(url)
    elif option == 3:
        os.chdir(path)
        try:
            os.mkdir(threadname)
        except:
            pass
        os.chdir(threadname)
        try:
            os.mkdir(time)
        except:
            pass

            
        os.chdir(time)
        wget.download(url)
        
        

def login_logout():
    global user_agent
    print(user_agent)
    cookies = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cookies_path = dir_path + "/session.json"
    try:
        # Load the session cookies
        if os.path.isfile(cookies_path):
            with open(cookies_path, 'r') as f:
                cookies = json.load(f)
    except:
        os.remove(cookies_path)
        # If it fails, never mind, we'll just login again
        # client = CustomClient(email, password, max_tries=1)
                
        
    if((not cookies) != True):
        client = CustomClient('email', 'password', user_agent=user_agent, session_cookies=cookies, logging_level = 30, max_tries=1)

    else:
        print("\n\nSaved credentials not found...\n\nEnter your Facebook credentials.\n\n(Don't worry, password will not be visible when typing! ;-) ")
        email = input("\nEmail/Phone/UserID: ")
        password = getpass("Password: ")
        print("\nIf you have Two Factor Authentication enabled in your account, enter then code when prompted.\n")

        client = CustomClient(email, password, user_agent=user_agent, logging_level = 30, max_tries=1)
    
    with open(cookies_path, 'w') as f:
        json.dump(client.getSession(), f)

    print("\nLogged in successfully\nListening for actions...")

    client.listen()

def down_print(count):
    if count == 1:
        print("\nDownloading 1st file...")
    elif count == 2:
        print("\nDownloading 2nd file...")
    elif count == 3:
        print("\nDownloading 3rd file...")
    else:
        print("\nDownloading " + str(count) + "th file...")
    
    
# for image, video, gif, attachment
def getMessageContent(self, t, messageObject, threadname):
    global option, count

    time1 = str(time.ctime()).replace(":", ".")
    if (messageObject.text == None or messageObject.text == '') and messageObject.sticker == None:
        print("\n\n" + str(len(messageObject.attachments)) + " file(s) have been queued for downloading!")
        for i in range(0, len(messageObject.attachments)):
            count += 1
            # If gif
            if hasattr(messageObject.attachments[i], 'animated_preview_url') and messageObject.attachments[i].animated_preview_url != None:

                url = self.fetchImageUrl(messageObject.attachments[i].uid)
                
                down_print(count)
                download(option, url, threadname, time1)

            # If normal image
            elif hasattr(messageObject.attachments[i], 'large_preview_url') and messageObject.attachments[i].large_preview_url != None:

                url = self.fetchImageUrl(messageObject.attachments[i].uid)

                down_print(count)
                download(option, url, threadname, time1)

            # If file attachment
            elif hasattr(messageObject.attachments[i], 'url') and messageObject.attachments[i].url != None:

                url = str(messageObject.attachments[i].url)
                # print(url)
                down_print(count)
                # os.chdir(path)
                # r = requests.head(url, allow_redirects=True)
                # print(r.url)
                # with open('file_name.pdf', 'wb') as f:
                #     f.write(r.content)
                # download(option, r, threadname, time1)
                download(option, url, threadname, time1)

            # If video
            elif hasattr(messageObject.attachments[i], 'preview_url') and messageObject.attachments[i].preview_url != None:
                url = messageObject.attachments[i].preview_url
                
                down_print(count)
                download(option, url, threadname, time1)
        count = 0   


class CustomClient(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):

        thread = self.fetchThreadInfo(thread_id)[thread_id]
        
        text = ''
        if thread_id == self.uid:
            text = getMessageContent(self, text, message_object, thread.name)
        

    def onReactionAdded(self, mid, reaction, author_id, thread_id, thread_type, ts, msg, **kwargs):
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        text = ''
        x = self.fetchMessageInfo(mid, thread_id)
        if author_id == self.uid:
            text = getMessageContent(self, text, x, thread.name)
            
            

        
    def onReactionRemoved(self, mid, author_id, thread_id, thread_type, ts, msg, **kwargs):
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        text = ''
        x = self.fetchMessageInfo(mid, thread_id)
        if author_id == self.uid:
            text = getMessageContent(self, text, x, thread.name)
 
 
login_logout()           
