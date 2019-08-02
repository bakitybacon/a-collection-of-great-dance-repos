#!/home/infrared/anaconda3/bin/python3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TRCK, TPE2, TDRC, TPOS
from mutagen.flac import FLAC

# mp3/id3 style tags
mp3coltags = {'Title': TIT2, 'Artist': TPE1, 'Album': TALB,
    'Genre': TCON, 'Track Number': TRCK, 'Album Artist': TPE2,
    'Year': TDRC, 'Disc Number': TPOS}

# flac/ogg style tags
flaccoltags = {'Title': 'title', 'Artist': 'artist', 'Album': 'album',
    'Genre': 'genre', 'Track Number': 'tracknumber',
    'Album Artist': 'albumartist', 'Year': 'date', 'Disc Number': 'discnumber'}

def writecolumn(musicdata, colstr):
    for idx, row in musicdata.iterrows():
        if row["Type"] == "MP3":
            filedata = ID3(row["Path"])
            filedata.add(mp3coltags[colstr](text=str(row[colstr])))
            filedata.save()
            print("Wrote to " + row["Path"] + "!")
        elif row["Type"] == "FLAC":
            filedata = FLAC(row["Path"])
            filedata.tags[flaccoltags[colstr]] = str(row[colstr])
            filedata.save()
            print("Wrote to " + row["Path"] + "!")
        else:
            error("Unknown Media Type!")
