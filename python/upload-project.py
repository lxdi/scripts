import subprocess
import os

version = "1.0"
print("Script version: %s" % version)

folderName = 'project-folder'
archiveName = 'project.tgz'
host = 'alex@ip'
keyPath = '~/.ssh/id_rsa'
targetDir = '/home/alex/Projects'


initDir = os.getcwd()

def prepCmd(cmd):
    if os.name == 'nt': return cmd.split()
    else: return cmd

def doCmd(cmd):
    cmd = prepCmd(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)

    for line in process.stdout:
    	print(line.decode('utf-8').replace('\n', ''))

    process.wait()

def doRemoteSsh(ssh):
    doCmd('ssh -i %s %s %s' % (keyPath, host, ssh))


print("-----------------------------------------Packing----------------------------------")
os.chdir('..')
doCmd('tar.exe --exclude=.git --exclude=.idea --exclude=target --exclude=localconf -zcvf localconf/%s .' % archiveName)
os.chdir(initDir)


print("-----------------------------------------Sending----------------------------------")
doCmd('scp -i %s -r %s %s:%s' % (keyPath, archiveName, host, targetDir))


print("-----------------------------------------Making dirs----------------------------------")
doRemoteSsh('mkdir -p %s/%s | exit' % (targetDir, folderName))

print("-----------------------------------------Unpacking----------------------------------")
doRemoteSsh('cd ~/Projects/sber ; tar -xf %s -C %s/ ; exit' % (archiveName, folderName))

print("---finish----")
