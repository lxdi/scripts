import os
import subprocess
from utils import utils
from utils import getch
from utils import filesColors

isDirsMode = True

extenders = {'q':'1', 'w':'2','e':'3','r':'4','t':'5','y':'6','u':'7','i':'8', 'o':'9', 'p':'0'}
columnWidth = 100

keys = {
'back': '-',
'exit': '\x18', #ctrl+x
'multiInput': '\x06', #ctrl+f
'switchMode': '\x01', #ctrl+a
'returnprev': '\x02' #ctrl+b
}

bindings = {
'h': '/home/alex',
'd': '/home/alex/Downloads',
'a': '/home/alex/Projects'
}

presets = {'video': 'vlc'}

defaultCommand = "mimeopen -n"
commandOnFile = defaultCommand

history = []

def changeCurrDir():
    global isDirsMode
    commandOnFile = defaultCommand
    history.append(os.getcwd())
    upperDivisor = '//////////////////////////////////////////////'
    print(("{0:"+str(columnWidth)+"} {1}").format(upperDivisor, upperDivisor))
    curDirsList = []
    curFilesList = []
    prevDirsList = []
    prevFilesList = []
    initLists(curDirsList, curFilesList, prevDirsList, prevFilesList)
    displayFiles(curDirsList, curFilesList, prevDirsList, prevFilesList)
    printCurrentDir()

    nextDirNum = getInputCustom()
    if keys['switchMode'] == nextDirNum: isDirsMode = not isDirsMode
    else:
        if isDirsMode: handleDirsMode(curDirsList, nextDirNum)
        else: handleFilesMode(curFilesList, nextDirNum)

    changeCurrDir()

def printCurrentDir():
    curDir = "%s %s %s" % ("\033[0;34m", os.getcwd(), "\033[0m")
    print(("{0} {1}").format(curDir, prevDirsFormat(4)))

def prevDirsFormat(offset):
    backDir = ''
    for i in range(2, offset+2):
        if len(history)>=i:
            backDir = backDir + "<- %s %s %s" % ("\033[0;36m", history[len(history)-i], "\033[0m")
    return backDir

def displayFiles(curDirs, curFiles, prevDirs, prevFiles):
    # for e in mergeLists(dirsList, filesList):
    #     print(e)
    curMerged = mergeLists(curDirs, curFiles, True)
    prevMerged = mergeLists(prevDirs, prevFiles, False)

    maxLen = 0
    if len(curMerged)>len(prevMerged):maxLen = len(curMerged)-1
    else: maxLen = len(prevMerged)-1

    for i in range(maxLen, -1, -1):
        dirStr = "\033[0;32m \033[0m"
        fileStr = "\033[0;32m \033[0m"
        if len(curMerged)>i:
            dirStr = curMerged[i]
            if len(dirStr)>columnWidth-7:
                dirStr = dirStr[:columnWidth-7]+'\033[0m'
        if len(prevMerged)>i:
            fileStr = prevMerged[i]
            if len(fileStr)>columnWidth-7:
                fileStr = fileStr[:columnWidth-7]+'\033[0m'
        print(("{0:"+str(columnWidth)+"} | {1}").format(dirStr, fileStr))

def mergeLists(dirs, files, isIndex):
        result = []

        if isDirsMode:
            formatInList(dirs, isIndex, result, isDirsMode, "\033[0;32m", True)
            result.append("\033[0;35m ------------------------------------ \033[0m")
            formatInList(files, False, result, isDirsMode, "\033[0;33m", False)
        else:
            formatInList(files, isIndex, result, isDirsMode, "\033[0;33m", False)
            result.append("\033[0;35m ------------------------------------ \033[0m")
            formatInList(dirs, False, result, isDirsMode, "\033[0;32m", True)
        return result

def formatInList(sourceList, isIndex, result, isUseExtenders, color, isDirs):
    for i in range(0, len(sourceList)):
        if isIndex:
            entry = replaceWithExtender(str(i)) if isUseExtenders else str(i)
            result.append("[%s] %s %s %s" % (entry, color if isDirs else filesColors.getColor(sourceList[i]),  sourceList[i], "\033[0m"))
        else: result.append("%s %s %s" % (color if isDirs else filesColors.getColor(sourceList[i]),  sourceList[i], "\033[0m"))


def initLists(curDirs, curFiles, prevDirs, prevFiles):
    initListsInPath(curDirs, curFiles, os.getcwd())
    # if os.getcwd() is not '/':
    #     initListsInPath(prevDirs, prevFiles, os.path.join(os.getcwd(), '..'))
    if len(history) > 1:
        initListsInPath(prevDirs, prevFiles, history[len(history)-2])

def initListsInPath(dirs, files, path):
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)): dirs.append(file)
        else: files.append(file)
    dirs.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)))
    dirs.reverse()
    files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)))
    files.reverse()

def replaceWithExtender(num):
    for key, value in extenders.items():
        if len(num)>1 and num.startswith(value):
            return num.replace(value, key, 1)
    return num

def getInputCustom():
    nextDirNum = ''
    if isDirsMode:
        nextDirNum = getch.getch()
        if nextDirNum == keys['multiInput']:
            nextDirNum = utils.askForInput("Cd to: ")
        if nextDirNum in extenders.keys():
            nextDirNum = extenders[nextDirNum] + getch.getch()
        if nextDirNum == '\n':
            nextDirNum = keys['switchMode']
    else:
        nextDirNum = utils.askForInput('Choose file(s): ')
        if nextDirNum.lower() == "":
            nextDirNum = keys['switchMode']
    handleExit(nextDirNum)
    return nextDirNum

def handleExit(num):
    if keys['exit'] == num:
        os.system("/bin/bash")
        exit(0)

def handleDirsMode(curDirsList, nextDirNum):
    if not checkKeys(nextDirNum):
        if checkBindings(nextDirNum) == False:
            if int(nextDirNum)<len(curDirsList):
                os.chdir(curDirsList[int(nextDirNum)])
            else: print('no such dir')

def checkKeys(nextDirNum):
    if keys['back'] == nextDirNum:
        os.chdir('..')
        return True
    if keys['returnprev'] == nextDirNum:
        os.chdir(history.pop()) # remove current
        if len(history) > 0:
            os.chdir(history.pop())
        return True
    return False

def checkBindings(input):
    if input in bindings.keys():
        os.chdir(bindings[input])
        return True
    else: return False

def handleFilesMode(filesList, inputString):
    global commandOnFile
    userCommand = False
    if '|' in inputString:
        userCommand = True
        splitted = inputString.split('|')
        inputString = splitted[0].strip()
        commandOnFile = splitted[1]

    for num in inputString.split(' '):
        if '-' in num:
            numsRange = num.split('-')
            for numFromRange in range(int(numsRange[0]), int(numsRange[1])+1):
                if not userCommand:
                    commandOnFile = checkPresets(filesList[numFromRange], commandOnFile)
                executeCommand(numFromRange, filesList, commandOnFile)
        else:
            if not userCommand:
                commandOnFile = checkPresets(filesList[int(num)], commandOnFile)
            executeCommand(int(num), filesList, commandOnFile)

def checkPresets(file, command):
    type = filesColors.checkType(file)
    if type in presets.keys():
        return presets[type]
    else: return command

def executeCommand(num, filesList, command):
    fileFullPath = os.path.join(os.getcwd(), filesList[num])
    fileFullPathEscaped = utils.escapeChars(fileFullPath)
    finalCommand = "%s %s" % (command, fileFullPathEscaped)

    print('Execute: ', finalCommand)
    process = subprocess.Popen([finalCommand], shell=True)

changeCurrDir()
