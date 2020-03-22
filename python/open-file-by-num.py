import subprocess
import os
import sys
from utils import utils

lastArg = ''
if len(sys.argv)>1:
    lastArg = sys.argv[len(sys.argv)-1]

lsCommand = "ls -t %s" % lastArg
commandOnFile = "mimeopen -n"

colors = {'red': '\033[0;31m', 'yellow': '\033[0;33m', 'blue': '\033[0;34m', 'white': '\033[0;37m',
 'magenta': '\033[0;35m', 'cyan': '\033[0;36m', 'green': '\033[0;32m', 'dgray': '\033[0;90m'}
closeColorTag = '\033[0m'

def displayFiles(filesList):
    num = len(filesList)-1
    for file in reversed(filesList):
        print("[%s] %s %s %s" % (num, colors[getColor(file)], file, closeColorTag))
        num = num - 1

def getColor(file):
    if checkName(file, ['.tar', '.zip', '.deb', '.exe', '.msi', '.rar', '.iso']): return 'yellow'
    if checkName(file, ['.mkv', '.mp4', '.avi', '.flac', '.mp3']): return 'blue'
    if checkName(file, ['.jpg', '.jpeg', '.png', '.gif']): return 'magenta'
    if checkName(file, ['.docx', '.xls', '.pdf', '.xmind']): return 'cyan'
    if checkName(file, ['.py', '.sh', '.java']): return 'red'
    if '.' in file: return 'green'
    else: return 'white'

def checkName(name, list):
    for substr in list:
        if substr in name.lower(): return True
    return False

def executeCommand(num, filesList, command):
    fileFullPath = os.path.join(os.getcwd(), filesList[num])
    fileFullPathEscaped = utils.escapeChars(fileFullPath)
    finalCommand = "%s %s" % (command, fileFullPathEscaped)

    print('Execute: ', finalCommand)
    process = subprocess.Popen([finalCommand], shell=True)
    # for line in process.stdout:
    #     print(line.decode('utf-8'))

chosenNums = []
filesList = utils.getFiles(lsCommand)
displayFiles(filesList)
print('------------------')
inputString = utils.askForInput("Choose a file (q to quit): ")

if '|' in inputString:
    splitted = inputString.split('|')
    inputString = splitted[0].strip()
    commandOnFile = splitted[1]

for num in inputString.split(' '):
    if '-' in num:
        numsRange = num.split('-')
        for numFromRange in range(int(numsRange[0]), int(numsRange[1])+1):
                executeCommand(numFromRange, filesList, commandOnFile)
    else:
        executeCommand(int(num), filesList, commandOnFile)
