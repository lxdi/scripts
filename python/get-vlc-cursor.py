import requests
import xml.etree.ElementTree as ET
#import pyperclip
from subprocess import Popen, PIPE
import subprocess
import time
import platform
import sys

debug = False

for arg in sys.argv[1:]:
    if arg == '-d':
        debug = True

pwd = "admin"
host = "localhost:8080"
sleepSc = 1
backOffsetSec = 10

def getMetadata():
    url = f"http://:{pwd}@{host}/requests/status.xml"
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        print(f'Error while reaching the server {e}')
    

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
    time.sleep(sleepSc)
    metadata = getMetadata()

    if metadata is None:
        continue

    cursor = getTime(metadata)
    copyToClipboard(cursor)

    if debug == True:
        print(f"Current time: {cursor}")