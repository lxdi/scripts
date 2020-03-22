import os
import subprocess
import sys

for arg in sys.argv[1:]:
    if arg == '--all':
        print('all pdf will be opened')

#files = []
for file in os.listdir(os.getcwd()):
        full_path_name = os.path.join(os.getcwd(), file)
        if os.path.splitext(full_path_name)[1] == '.pdf':
            print(full_path_name)
            process = subprocess.Popen(['mimeopen', '-n', full_path_name])
            #files.append(full_path_name)
