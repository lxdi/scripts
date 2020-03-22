import os
import subprocess
from utils import utils
from utils import getch
from utils import filesColors
from utils import tab

isDirsMode = True
isLeftTab = True

extenders = {'q':'1', 'w':'2','e':'3','r':'4','t':'5','y':'6','u':'7','i':'8', 'o':'9', 'p':'0'}
columnWidth = 100

keys = {
'back': '-',
'exit': '\x18', #ctrl+x
'multiInput': '\x06', #ctrl+f
'switchMode': '\x01', #ctrl+a
'returnprev': '\x02', #ctrl+b
'switchTabs': '\t' #tab
}

bindings = {
'h': '/home/alex',
'd': '/home/alex/Downloads',
'a': '/home/alex/Projects'
}

presets = {'video': 'vlc'}

defaultCommand = "mimeopen -n"
commandOnFile = defaultCommand

leftTab = tab.Tab()
rightTab = tab.Tab()

def changeCurrDir():
    global isDirsMode
    global isLeftTab
    commandOnFile = defaultCommand
    upperDivisor = '//////////////////////////////////////////////'
    print(("{0:"+str(columnWidth)+"} {1}").format(upperDivisor, upperDivisor))

    if isLeftTab: leftTab.history.append(leftTab.cwd)
    else: rightTab.history.append(rightTab.cwd)

    initLists(leftTab)
    initLists(rightTab)
    displayFiles(leftTab, rightTab)

    if isLeftTab: printCurrentDir(leftTab)
    else: printCurrentDir(rightTab)

    nextDirNum = getInputCustom()
    if keys['switchTabs'] == nextDirNum: isLeftTab = not isLeftTab
    else:
        if keys['switchMode'] == nextDirNum: isDirsMode = not isDirsMode
        else:
            if isDirsMode: handleDirsMode(leftTab if isLeftTab else rightTab, nextDirNum)
            else: handleFilesMode(leftTab if isLeftTab else rightTab, nextDirNum)

    changeCurrDir()

def printCurrentDir(tab):
    curDir = "%s %s %s" % ("\033[0;34m", tab.cwd, "\033[0m")
    print(("{0} {1}").format(curDir, prevDirsFormat(tab, 4)))

def prevDirsFormat(tab, offset):
    backDir = ''
    for i in range(2, offset+2):
        if len(tab.history)>=i:
            backDir = backDir + "<- %s %s %s" % ("\033[0;36m", tab.history[len(tab.history)-i], "\033[0m")
    return backDir

def displayFiles(leftTab, rightTab):
    # for e in mergeLists(dirsList, filesList):
    #     print(e)
    curMerged = mergeLists(leftTab.curDirsList, leftTab.curFilesList, True if isLeftTab else False)
    prevMerged = mergeLists(rightTab.curDirsList, rightTab.curFilesList, True if not isLeftTab else False)

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

def initLists(tab):
    tab.curDirsList = []
    tab.curFilesList = []
    for file in os.listdir(tab.cwd):
        if os.path.isdir(os.path.join(tab.cwd, file)): tab.curDirsList.append(file)
        else: tab.curFilesList.append(file)
    tab.curDirsList.sort(key=lambda x: os.path.getmtime(os.path.join(tab.cwd, x)))
    tab.curDirsList.reverse()
    tab.curFilesList.sort(key=lambda x: os.path.getmtime(os.path.join(tab.cwd, x)))
    tab.curFilesList.reverse()

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

def handleDirsMode(tab, nextDirNum):
    if not checkKeys(tab, nextDirNum):
        if checkBindings(tab, nextDirNum) == False:
            if int(nextDirNum)<len(tab.curDirsList):
                tab.cwd = os.path.join(tab.cwd, tab.curDirsList[int(nextDirNum)])
            else: print('no such dir')

def checkKeys(tab, nextDirNum):
    if keys['back'] == nextDirNum:
        tab.cwd = os.path.join(tab.cwd, '..')
        return True
    if keys['returnprev'] == nextDirNum:
        tab.history.pop() # remove current
        if len(history) > 0:
            tab.cwd = tab.history.pop()
        return True
    return False

def checkBindings(tab, input):
    if input in bindings.keys():
        tab.cwd = bindings[input]
        return True
    else: return False

def handleFilesMode(tab, inputString):
    global commandOnFile
    userCommand = False
    if '|' in inputString:
        userCommand = True
        splitted = inputString.split('|')
        inputString = splitted[0].strip()
        commandOnFile = splitted[1]

    inputString = inputString.strip()
    for num in inputString.split(' '):
        if '-' in num:
            numsRange = num.split('-')
            for numFromRange in range(int(numsRange[0]), int(numsRange[1])+1):
                if not userCommand:
                    commandOnFile = checkPresets(tab.curFilesList[numFromRange], commandOnFile)
                executeCommand(tab, numFromRange, commandOnFile)
        else:
            if not userCommand:
                commandOnFile = checkPresets(tab.curFilesList[int(num)], commandOnFile)
            executeCommand(tab, int(num), commandOnFile)

def checkPresets(file, command):
    type = filesColors.checkType(file)
    if type in presets.keys():
        return presets[type]
    else: return command

def executeCommand(tab, num, command):
    fileFullPath = os.path.join(tab.cwd, tab.curFilesList[num])
    fileFullPathEscaped = utils.escapeChars(fileFullPath)
    finalCommand = "%s %s" % (command, fileFullPathEscaped)

    print('Execute: ', finalCommand)
    process = subprocess.Popen([finalCommand], shell=True)

changeCurrDir()
