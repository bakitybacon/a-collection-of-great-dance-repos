#!/home/infrared/anaconda3/bin/python3
from mutagen.id3 import ID3
from mutagen.flac import FLAC
import pandas as pd
import sys
import subprocess
import re

# deal with mp3 files first

pathbytes = subprocess.check_output('find "`pwd`" -name "*.mp3"', shell=True)
paths = pathbytes.decode().split("\n")[:-1]

id3tags = {'TIT2': 'Title', 'TPE1': 'Artist', 'TALB': 'Album', 'TCON': 'Genre', 'TRCK': 'Track Number', 'TPE2': 'Album Artist', 'TDRC': 'Year', 'TPOS': 'Disc Number'}

columns = {}
for value in id3tags.values():
    columns[value] = []
columns['Path'] = []
columns['Type'] = []

for path in paths:
    songdata = ID3(path)
    for tag, colname in id3tags.items():
        if tag in songdata:
            if colname == 'Disc Number' or colname == 'Track Number':
                columns[colname].append(int(str(songdata[tag]).split('/')[0]))
            else:
                columns[colname].append(songdata[tag])
        else:
            if colname == 'Disc Number':
                columns[colname].append(1)
            else:
                columns[colname].append('~~ MISSING ~~')
    columns['Path'].append(path)
    columns['Type'].append('MP3')

# flac files

flactags = {'title': 'Title', 'artist': 'Artist', 'album': 'Album', 'genre':
    'Genre', 'tracknumber': 'Track Number', 'albumartist': 'Album Artist',
    'date': 'Year', 'discnumber': 'Disc Number'}

# TODO: deal with the case where multiple possible tags give same info
#   eg: disc + discnumber

pathbytes = subprocess.check_output('find "`pwd`" -name "*.flac"', shell=True)
paths = pathbytes.decode().split("\n")[:-1]

for path in paths:
    songdata = FLAC(path)

    for tag, val in songdata.tags.items():
        newtag = re.sub('[^a-z]', '', tag.lower())
        if tag != newtag:
            songdata[newtag] = val
            del songdata[tag]

    for tag, colname in flactags.items():
        if tag in songdata:
            if colname == 'Disc Number' or colname == 'Track Number':
                columns[colname].append(int(str(list(songdata[tag])[0]).split('/')[0]))
            else:
                columns[colname].append(list(songdata[tag])[0])
        else:
            if colname == 'Disc Number':
                columns[colname].append(1)
            else:
                columns[colname].append('~~ MISSING ~~')
    columns['Path'].append(path)
    columns['Type'].append("FLAC")

music = pd.DataFrame(columns)
music.to_csv("musicdb.csv")
