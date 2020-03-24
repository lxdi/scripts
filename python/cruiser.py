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
'minus': '-',
'exit': '\x18', #ctrl+x
'multiInput': '\x06', #ctrl+f
'switchMode': '\r', #'\x01', #ctrl+a
'returnprev': '\x02', #ctrl+b
'switchTabs': '\t', #tab
'arrowUp': '\x1b[A',
'arrowDown': '\x1b[B',
'arrowRight': '\x1b[C',
'arrowLeft': '\x1b[D',
}

substitutions = {
    'leftTabDir': '$dl',
    'rightTabDir': '$dr',
    'fileName': '$f',
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
    os.system('clear')
    commandOnFile = defaultCommand
    upperDivisor = '//////////////////////////////////////////////'
    print(("{0:"+str(columnWidth)+"} {1}").format(upperDivisor, upperDivisor))

    curTab = leftTab if isLeftTab else rightTab

    initLists(leftTab)
    initLists(rightTab)
    displayFiles(leftTab, rightTab)
    printCurrentDir(curTab)

    nextDirNum = getInputCustom()
    if not handleSwitches(nextDirNum, curTab):
        if isDirsMode: handleDirsMode(leftTab if isLeftTab else rightTab, nextDirNum)
        else: handleFilesMode(leftTab if isLeftTab else rightTab, nextDirNum)

    changeCurrDir()

def handleSwitches(nextDirNum, tab):
    global isDirsMode
    global isLeftTab
    if keys['switchTabs'] == nextDirNum:
        isLeftTab = not isLeftTab
        return True
    if keys['switchMode'] == nextDirNum:
        isDirsMode = not isDirsMode
        return True
    if keys['arrowUp'] == nextDirNum:
        if tab.subcursor >-1: tab.subcursor = changeCursor(tab.subcursor, 2, True)
        else: tab.cursor = changeCursor(tab.cursor, len(tab.curDirsList)-1, True)
        return True
    if keys['arrowDown'] == nextDirNum:
        if tab.subcursor >-1: tab.subcursor = changeCursor(tab.subcursor, 2, False)
        else: tab.cursor = changeCursor(tab.cursor, len(tab.curDirsList)-1, False)
        return True
    if keys['minus'] == nextDirNum:
        if tab.subcursor == -1: tab.subcursor = 0
        else: tab.subcursor = -1
        return True
    return False

def changeCursor(cursorInit, maxNum, isAugment):
    if isAugment:
        if cursorInit == maxNum: return maxNum
        else: return cursorInit + 1
    else:
        if cursorInit == 0: return 0
        else: return cursorInit - 1


def printCurrentDir(tab):
    curDir = "%s %s %s" % ("\033[0;34m", tab.cwd, "\033[0m")
    print(("{0} {1}").format(curDir, prevDirsFormat(tab, 4)))

def prevDirsFormat(tab, offset):
    backDir = ''
    for i in range(1, offset+2):
        if len(tab.history)>=i:
            backDir = backDir + "<- %s %s %s" % ("\033[0;36m", tab.history[len(tab.history)-i], "\033[0m")
    return backDir

def displayFiles(leftTab, rightTab):
    # for e in mergeLists(dirsList, filesList):
    #     print(e)
    curMerged = mergeLists(leftTab.curDirsList, leftTab.curFilesList, True if isLeftTab else False, leftTab.cursor, leftTab.subcursor)
    prevMerged = mergeLists(rightTab.curDirsList, rightTab.curFilesList, True if not isLeftTab else False, rightTab.cursor, rightTab.subcursor)

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

def mergeLists(dirs, files, isIndex, cursor, subcursor):
        result = []
        if isDirsMode:
            formatInList(dirs, isIndex, result, isDirsMode, "\033[0;32m", True, cursor, subcursor)
            result.append("\033[0;35m ------------------------------------ \033[0m")
            formatInList(files, False, result, isDirsMode, "\033[0;33m", False, cursor, subcursor)
        else:
            formatInList(files, isIndex, result, isDirsMode, "\033[0;33m", False, cursor, subcursor)
            result.append("\033[0;35m ------------------------------------ \033[0m")
            formatInList(dirs, False, result, isDirsMode, "\033[0;32m", True, cursor, subcursor)
        return result

def formatInList(sourceList, isIndex, result, isUseExtenders, color, isDirs, cursor, subcursor):
    edge = 50
    for i in range(0, len(sourceList) if len(sourceList)<edge else edge ):
        if isIndex:
            if cursor == i and subcursor > -1:
                for j, subEntry in enumerate(['Copy', 'Move', 'Delete']):
                    result.append("  \033[0;35m %s| %s |%s \033[0m" % ('>' if j==subcursor else ' ',  subEntry, '<' if j==subcursor else ' '))
            entry = replaceWithExtender(str(i)) if isUseExtenders else str(i)
            result.append("%s[%s] %s %s %s" % ('>' if cursor == i else '', entry, color if isDirs else filesColors.getColor(sourceList[i]),  sourceList[i], "\033[0m"))
        else: result.append("%s %s %s" % (color if isDirs else filesColors.getColor(sourceList[i]),  sourceList[i], "\033[0m"))

def initLists(tab):
    if tab.dirtyLists:
        tab.curDirsList = []
        tab.curFilesList = []
        for file in os.listdir(tab.cwd):
            if os.path.isdir(os.path.join(tab.cwd, file)): tab.curDirsList.append(file)
            else: tab.curFilesList.append(file)
        tab.curDirsList.sort(key=lambda x: os.path.getmtime(os.path.join(tab.cwd, x)))
        tab.curDirsList.reverse()
        tab.curFilesList.sort(key=lambda x: os.path.getmtime(os.path.join(tab.cwd, x)))
        tab.curFilesList.reverse()
        tab.dirtyLists = False

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
        if isLeftTab: os.chdir(leftTab.cwd)
        else: os.chdir(rightTab.cwd)
        os.system("/bin/bash")
        exit(0)

def handleDirsMode(tab, nextDirNum):
    if not checkKeys(tab, nextDirNum):
        if checkBindings(tab, nextDirNum) == False:
            if int(nextDirNum)<len(tab.curDirsList): tab.changeDir(os.path.join(tab.cwd, tab.curDirsList[int(nextDirNum)]))
            else: print('no such dir')

def checkKeys(tab, nextDirNum):
    if keys['arrowLeft'] == nextDirNum:
        #tab.cwd = os.path.join(tab.cwd, os.pardir)
        tab.changeDir(os.path.dirname(tab.cwd))
        return True
    if keys['returnprev'] == nextDirNum:
        tab.popHistory()
        return True
    if keys['arrowRight'] == nextDirNum:
        if tab.subcursor >-1: print('todo handle move/copy/delete')
        else: tab.changeDir(os.path.join(tab.cwd, tab.curDirsList[tab.cursor]))
        return True
    return False

def checkBindings(tab, input):
    if input in bindings.keys():
        tab.changeDir(bindings[input])
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
    finalCommand = handleSubstitutions(tab, num, command)
    if finalCommand is None:
        fileFullPath = os.path.join(tab.cwd, tab.curFilesList[num])
        fileFullPathEscaped = utils.escapeChars(fileFullPath)
        finalCommand = "%s %s" % (command, fileFullPathEscaped)

    print('Execute: ', finalCommand)
    process = subprocess.Popen([finalCommand], shell=True)

def handleSubstitutions(tab, num, command):
    result = False
    finalCommand = command
    if substitutions['fileName'] in finalCommand:
        result = True
        finalCommand = finalCommand.replace(substitutions['fileName'], utils.escapeChars(tab.curFilesList[num]))
    if substitutions['leftTabDir'] in finalCommand:
        result = True
        finalCommand = finalCommand.replace(substitutions['leftTabDir'], utils.escapeChars(leftTab.cwd))
    if substitutions['rightTabDir'] in finalCommand:
        result = True
        finalCommand = finalCommand.replace(substitutions['rightTabDir'], utils.escapeChars(rightTab.cwd))
    if result: return finalCommand
    else: return None

changeCurrDir()
