
colors = {'red': '\033[0;31m', 'yellow': '\033[0;33m', 'blue': '\033[0;34m', 'white': '\033[0;37m',
 'magenta': '\033[0;35m', 'cyan': '\033[0;36m', 'green': '\033[0;32m', 'dgray': '\033[0;90m'}
closeColorTag = '\033[0m'

colorSchemeForFiles = {'archive': 'yellow', 'video': 'blue', 'music': 'blue', 'image': 'magenta', 'executable': 'red', 'document': 'cyan'}

def getColor(file):
    return colors[getColorName(file)]

def getColorName(file):
    if checkType(file) in colorSchemeForFiles.keys():
        return colorSchemeForFiles[checkType(file)]
    if '.' in file: return 'green'
    else: return 'white'

def checkType(file):
    if checkName(file, ['.tar', '.zip', '.deb', '.exe', '.msi', '.rar', '.iso']): return 'archive'
    if checkName(file, ['.mkv', '.mp4', '.avi', '.mov', '.flv', '.m4v']): return 'video'
    if checkName(file, ['.flac', '.mp3']): return 'music'
    if checkName(file, ['.jpg', '.jpeg', '.png', '.gif']): return 'image'
    if checkName(file, ['.docx', '.xls', '.pdf', '.xmind']): return 'document'
    if checkName(file, ['.py', '.sh', '.java']): return 'executable'
    return 'other'

def checkName(name, list):
    for substr in list:
        if substr in name.lower(): return True
    return False
