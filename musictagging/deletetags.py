#!/home/infrared/anaconda3/bin/python3
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
import subprocess
import re

# deal with mp3 files first
pathbytes = subprocess.check_output(
    'find "/media/infrared/789D52821263E12D/musicworkspace" -name "*.mp3"',
    shell=True)
paths = pathbytes.decode().split("\n")[:-1]

deltags = {'COMM::\x00\x00\x00': 'Comment', 'TENC': 'Encoded By',
    'UFID': 'Text', 'TXXX': 'Misc Text', 'WXXX:': 'URL',
    'TSSE': 'Encoder Settings', 'TDRL': 'YMD Date (too specific)',
    'PRIV': 'private tag'}
id3tags = {'TIT2': 'Title', 'TPE1': 'Artist', 'TALB': 'Album', 'TCON': 'Genre',
    'TRCK': 'Track Number', 'TPE2': 'Album Artist', 'TDRC': 'Year',
    'TPOS': 'Disc Number', 'TCOM': 'Composer'}

for path in paths:
    songdata = ID3(path)
    mp3data = MP3(path)
    changed = False

    for tag, colname in deltags.items():
        if tag in songdata:
            songdata.delall(tag)
            changed = True
            print("deleted " + colname + " from " + path + "!")

    for key in mp3data.tags.keys():
        if key not in deltags and key not in id3tags and not key[:4] == "APIC":
            print("unknown key!", key)

    if changed:
        songdata.save()

# flac files

pathbytes = subprocess.check_output(
    'find "/media/infrared/789D52821263E12D/musicworkspace" -name "*.flac"',
    shell=True)
paths = pathbytes.decode().split("\n")[:-1]

flactags = {'title': 'Title', 'artist': 'Artist', 'album': 'Album', 'genre':
    'Genre', 'tracknumber': 'Track Number', 'albumartist': 'Album Artist',
    'date': 'Year', 'discnumber': 'Disc Number', 'disc': 'Disc Number'}

deltags = {'description': 'comment', 'comment': 'comment',
    'tool name': 'toolname', 'tool version': 'random',
    'hdtracks': 'some garbage', 'country': 'country',
    'catalogid': 'catalog id', 'organization': 'organization',
    'style': 'subgenre i guess?', 'originalyear': 'just use year',
    'originaldate': 'why'}

for path in paths:
    songdata = FLAC(path)

    for tag, val in songdata.tags.items():
        newtag = re.sub('[^a-z]', '', tag.lower())
        if tag != newtag:
            songdata[newtag] = val
            del songdata[tag]

    changed = False

    for tag, colname in deltags.items():
        if tag in songdata:
            del songdata.tags[tag]
            changed = True
            print("deleted " + colname + " from " + path + "!")

    for key in songdata.tags.keys():
        if key not in deltags and key not in flactags:
            print("unknown key!", key)

    if changed:
        songdata.save()
