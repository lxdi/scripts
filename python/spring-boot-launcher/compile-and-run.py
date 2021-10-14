import subprocess
import os

version = "1.2"
print("Script version: %s" % version)

pidFileName = 'pid.file'
if os.path.isfile(pidFileName):
	print('--------------------- Shutting down previous --------------------------------')
	for line in open(pidFileName):
		pid = line
	shutdownCmd = 'kill %s' % pid
	shutdownprocess = subprocess.Popen(shutdownCmd, shell=True)
	shutdownprocess.wait()
	os.remove(pidFileName)
	print('Shutdown: done')


print("-----------------------------------------Compilation----------------------------------")
initDir = os.getcwd()
os.chdir('..')
process = subprocess.Popen(['./gradlew clean bootJar'], shell=True, stdout = subprocess.PIPE)

for line in process.stdout:
	print(line.decode('utf-8').replace('\n', ''))

process.wait()
os.chdir(initDir)

print("-----------------------------------------Starting----------------------------------")

debugPort = '5005'
debugOption = '-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=%s' % debugPort
shutdownOption = '& echo $! > ./%s' % pidFileName

jarFolder = os.path.join(os.getcwd(), '..', 'backend', 'build', 'libs')
jarPath = os.path.join(jarFolder, os.listdir(jarFolder)[0])

processJava = subprocess.Popen('java %s -jar %s %s' % (debugOption, jarPath, shutdownOption), shell=True)
print('Started with pid ' + str(processJava.pid))
