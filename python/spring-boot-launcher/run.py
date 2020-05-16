import subprocess
import os

version = "1.0"
print("Script version: %s" % version)

debugPort = '5880'
debugOption = '-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=%s' % debugPort
pidFileName = 'pid.file'
shutdownOption = '& echo $! > ./%s' % pidFileName
warPath = os.path.join(os.getcwd(), 'ROOT.jar')
processjava = subprocess.Popen('java %s -jar %s %s' % (debugOption, warPath, shutdownOption), shell=True)
print('Started wiht pid ' + str(processjava.pid))
