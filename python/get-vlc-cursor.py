import requests
import xml.etree.ElementTree as ET
#import pyperclip
from subprocess import Popen, PIPE
import subprocess
import time
import platform


pwd = "admin"
host = "localhost:8080"
sleepSc = 1
backOffsetSec = 10

def getMetadata():
    url = f"http://:{pwd}@{host}/requests/status.xml"
    response = requests.get(url)
    return response.text

def getTime(xml):
    timeEl = ET.fromstring(xml).find('time')

    if timeEl is not None:
        secs = int(timeEl.text) - backOffsetSec
        return formatSeconds(secs, 'withSeconds_full')

def formatSeconds(s, formatType):
    match formatType:
        case 'withSeconds':
            return '{:02}:{:02}:{:02}'.format(s//3600, s%3600//60, s%60)
        case 'withSeconds_full':
            return '{:02}:{:02}:{:02} - '.format(s//3600, s%3600//60, s%60)
        case _:
            return '{:02}:{:02}'.format(s//3600, s%3600//60)

def copyToClipboard(text):
    match platform.system():
        case "Linux":
            return copyToClipBoardLinux(text)
        case "Darwin":
            return copyToClipBoardMac(text)


def copyToClipBoardLinux(text):
    p = Popen(['xsel','-bi'], stdin=PIPE)
    p.communicate(input=text.encode())

def copyToClipBoardMac(text):
    #pyperclip.copy("test")
    subprocess.run("pbcopy", text=True, input=text)

while True:
    cursor = getTime(getMetadata())
    copyToClipboard(cursor)
    time.sleep(sleepSc)
    print(f"Current time: {cursor}")