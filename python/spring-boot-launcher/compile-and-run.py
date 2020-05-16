import subprocess
import os

version = "1.1"
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

debugPort = '5005'
debugOption = '-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=%s' % debugPort
shutdownOption = '& echo $! > ./%s' % pidFileName
warPath = os.path.join(os.getcwd(), '..', 'backend', 'build', 'libs', 'ROOT.jar')
processjava = subprocess.Popen('java %s -jar %s %s' % (debugOption, warPath, shutdownOption), shell=True)
print('Started wiht pid ' + str(processjava.pid))
