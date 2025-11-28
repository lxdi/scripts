import subprocess
import os

def prepCmd(cmd):
    if os.name == 'nt': return cmd.split()
    else: return cmd

def doCmd(cmd):
    cmd = prepCmd(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)

    for line in process.stdout:
    	print(line.decode('utf-8').replace('\n', ''))

    process.wait()

def doRemoteSsh(host, keyPath, ssh):
    doCmd('ssh -i %s %s %s' % (keyPath, host, ssh))