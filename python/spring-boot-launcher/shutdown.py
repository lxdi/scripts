import subprocess
import os

shutdownCmd = 'kill $(cat ./pid.file)'
processjava = subprocess.Popen(shutdownCmd, shell=True)
print('Shutdown: done')
