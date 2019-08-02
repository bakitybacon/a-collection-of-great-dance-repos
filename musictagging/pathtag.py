#!/home/infrared/anaconda3/bin/python3
from mutagen.id3 import ID3, TPE2, TPOS
from mutagen.flac import FLAC
import subprocess

# deal with mp3 files first

pathbytes = subprocess.check_output('find "/media/infrared/789D52821263E12D/Music Library/" -name "*.mp3"', shell=True)
paths = pathbytes.decode().split("\n")[:-1]

pathtags = {'TIT2': 'Title', 'TALB': 'Album', 'TRCK': 'Track Number', 'TPE2': 'Album Artist', 'TPOS': 'Disc Number'}

for path in paths:
    songdata = ID3(path)

    pathdata = path[len("/media/infrared/789D52821263E12D/Music Library/"):].split("/")
    trackdata = pathdata[2].split("-", 2)

    print(path)

    albumartist = pathdata[0]
    albumname = pathdata[1]
    discnum = trackdata[0]
    tracknum = trackdata[1]
    tracktitle = trackdata[2]

    songdata.add(TPE2(text=albumartist))
    songdata.add(TPOS(text=discnum))

    songdata.save()
