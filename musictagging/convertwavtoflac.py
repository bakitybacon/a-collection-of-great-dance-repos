#!/home/infrared/anaconda3/bin/python3
import subprocess
from pydub import AudioSegment

# find all wav files
pathbytes = subprocess.check_output('find "`pwd`" -name "*.wav"', shell=True)
paths = pathbytes.decode().split("\n")[:-1]

for path in paths:
    song = AudioSegment.from_wav(path)
    song.export(path[:-4] + ".flac",format = "flac")

