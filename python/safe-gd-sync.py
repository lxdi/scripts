import subprocess
import json
from dateutil.parser import parse
import time
import os
import datetime

localStoragePath = '/home/alex/google-drive'
cloudPath = 'google-drive:/'

latestModTimeGd = None
latestModTimeLocal = None

start_time = time.time()

def checkOnCloud():
    global latestModTimeGd
    jsonstring = ""
    process = subprocess.Popen(["rclone lsjson %s -R" % cloudPath], shell=True, stdout = subprocess.PIPE)
    for line in process.stdout:
        #print(line)
        jsonstring = jsonstring + line.decode('utf-8')

    objects = json.loads(jsonstring)

    for obj in objects:
        modTime = parse(obj['ModTime']).replace(tzinfo=None)
        if latestModTimeGd is None or latestModTimeGd<modTime:
            latestModTimeGd = modTime

def getLastModifiedDate(dir):
    files = os.listdir(dir)
    for fileName in files:
        fileFullPath = os.path.join(dir, fileName)
        checkLastModDate(fileFullPath)
        if not os.path.isfile(fileFullPath):
            getLastModifiedDate(fileFullPath)


def checkLastModDate(fullPath):
    global latestModTimeLocal
    modDate = datetime.datetime.utcfromtimestamp(os.path.getmtime(fullPath))
    if latestModTimeLocal is None or modDate > latestModTimeLocal:
        latestModTimeLocal = modDate

checkOnCloud()
getLastModifiedDate(os.path.join(localStoragePath))

print("-----GD: %s-------------" % latestModTimeGd)
print("-----Local: %s-------------" % latestModTimeLocal)

if latestModTimeLocal > latestModTimeGd:
    print('Local files are up to date')
else:
    print('Google drive is up to date ')


print("--- %s seconds ---" % (time.time() - start_time))
