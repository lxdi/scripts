import subprocess
import os

pidFileName = 'pid.file'
file = open(pidFileName)
for line in file:
    pid = line

shutdownCmd = 'kill %s' % pid
processjava = subprocess.Popen(shutdownCmd, shell=True)
print('Shutdown: done')

os.remove(pidFileName)
