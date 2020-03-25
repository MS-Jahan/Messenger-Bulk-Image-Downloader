import os
import time
import traceback
import json
from fbchat import Client
from fbchat.models import *
import wget
from getpass import getpass
import os.path


dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
print(os.path.basename(__file__))

ua_file_path = dir_path + "\\ua.txt"

print("##################################\nMessenger Image Bulk Downloader\n##################################\n")
print("Not only images, you can download files from Messenger by reacting to messages, forwarding to your own conversation or just simply save all whoever sends you something.")
print("Images, GIFs, Videos and other attachments will be saved at \"MessIm\" folder in Desktop.\n")
option = int(input("Select an option:\n1) Save all images in one folder.\n2) Save images conversation name-wise.\n3) Save images conversation name-wise and time-wise.\n\nYour Choice: "))


if os.path.exists(ua_file_path) == False: 
    user_agent = input('\n\nPlease enter the user agent of the browser you usually login to facebook. Just goto https://www.whatsmyua.info/, copy the text, paste here and press enter.\n\nYour browser\'s user agent will be something like this:\nMozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36\n\nUser agent is needed to fake this program as a normal browser you use, so that your account remains human-like to Facebook. You\'ll not have to enter the user agent every time you use this program. :-)\n\nUser agent: ')
    with open(ua_file_path, "w") as ua:
        ua.write(user_agent)
else:
    with open(ua_file_path, 'r') as ua:
        user_agent = ua.read().replace('\n', '')

       
count = 0

def download(option, url, threadname, time):
    path = str(os.environ["HOMEPATH"]) + "\\Desktop\\MessIm"
    try:
        os.mkdir(path)
    except:
        pass

    if option == 1:
        os.chdir(path)
        wget.download(url)
    elif option == 2:
        try:
            os.mkdir(path + "\\" + threadname)
        except:
            pass
        os.chdir(path + "\\" + threadname)
        wget.download(url)
    elif option == 3:
        try:
            os.mkdir(path + "\\" + threadname)
        except:
            pass
        
        try:
            os.mkdir(path + "\\" + threadname + "\\" + time)
        except:
            pass
            
            
        os.chdir(path + "\\" + str(threadname) + "\\" + time)
        wget.download(url)
        
        

def login_logout():
    cookies = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cookies_path = dir_path + "\\session.json"
    try:
        # Load the session cookies
        if os.path.isfile(cookies_path):
            with open(cookies_path, 'r') as f:
                cookies = json.load(f)
    except:
        os.remove('session.json')
        # If it fails, never mind, we'll just login again
        # client = CustomClient(email, password, max_tries=1)
                
        
    if((not cookies) != True):
        client = CustomClient('email', 'password', user_agent=user_agent, session_cookies=cookies, logging_level = 30, max_tries=1)

    else:
        print("\n\nSaved credentials not found...\n\nEnter your Facebook credentials.\n(Don't worry, password will not be visible when typing! ;-) ")
        email = input("Email/Phone/UserID: ")
        password = getpass("Password: ")
        print("\nIf you have Two Factor Authentication enabled in your account, enter then code when prompted.\n")

        
        client = CustomClient(email, password, user_agent=user_agent, logging_level = 30, max_tries=1)
    
    with open('session.json', 'w') as f:
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

                down_print(count)
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
