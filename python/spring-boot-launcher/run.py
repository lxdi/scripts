import subprocess
import os

debugPort = '5005'
warPath = os.path.join(os.getcwd(), 'ROOT.jar')
shutdownOption = '& echo $! > ./pid.file'
processjava = subprocess.Popen('java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=%s -jar %s %s' % (debugPort, warPath, shutdownOption), shell=True)
print('Started with pid: ' + str(processjava.pid))

