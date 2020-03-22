import subprocess
import os

def askForInput(text):
    inputString = input(text)
    if inputString is 'q':
        os.system("/bin/bash")
        exit(0)
    return inputString

def getFiles(lsCommand):
    filesList = []
    process = subprocess.Popen([lsCommand], shell=True, stdout = subprocess.PIPE)
    for line in process.stdout: filesList.append(line.decode('utf-8').replace('\n', ''))
    return filesList

def escapeChars(str):
    return str.replace(' ', '\\ ').replace('(', '\\(').replace(')', '\\)').replace('[', '\\[').replace(']', '\\]').replace(',', '\\,').replace('&', '\\&')

def getFilesExtended(lsCommand):
    filesList = []
    process = subprocess.Popen([lsCommand], shell=True, stdout = subprocess.PIPE)
    for line in process.stdout:
        file = {}
        lineSplitted = line.decode('utf-8').replace('\n', '').split(' ')
        file['name'] = lineSplitted[len(lineSplitted)-1]
        filesList.append(file)
    return filesList
