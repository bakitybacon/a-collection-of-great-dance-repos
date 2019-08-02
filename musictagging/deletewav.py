#!/home/infrared/anaconda3/bin/python3
import subprocess
import os

# find all wav files
pathbytes = subprocess.check_output('find "`pwd`" -name "*.wav"', shell=True)
paths = pathbytes.decode().split("\n")[:-1]

for path in paths:
    os.remove(path)

