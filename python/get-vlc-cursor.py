import requests
import xml.etree.ElementTree as ET
import pyperclip
from subprocess import Popen, PIPE


pwd = "admin"
host = "localhost:8080"


url = f"http://:{pwd}@{host}/requests/status.xml"
response = requests.get(url)

#print(response.text)

root = ET.fromstring(response.text)

timeEl = root.find('time')

if timeEl is not None:
    s = int(timeEl.text)
    timeFormatted = '{:02}:{:02}'.format(s//3600, s%3600//60)
    #pyperclip.copy("test")
    #subprocess.run("pbcopy", text=True, input=timeFormatted)
    p = Popen(['xsel','-bi'], stdin=PIPE)
    p.communicate(input=timeFormatted.encode())
    print(f"Current time: {timeFormatted}")