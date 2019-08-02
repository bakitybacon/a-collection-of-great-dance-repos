#!/home/infrared/anaconda3/bin/python3
import pandas as pd
import os
import subprocess
import shutil
import re

music = pd.read_csv("musicdb.csv")
basepath = os.getcwd() + "/reorganized/"

for idx, row in music.iterrows():
    # make sure our file names are acceptable
    fixtitle = re.sub('[^\w\s-]', '_', row['Title'])
    fixalbartist = re.sub('[^\w\s-]', '_', row['Album Artist'])
    fixalbtitle = re.sub('[^\w\s-]', '_', row['Album'])

    destdir = basepath + fixalbartist + '/' + fixalbtitle + '/'
    destfile = '{:02d}'.format(row['Disc Number']) + ' - ' + '{:02d}'.format(row['Track Number']) + ' - ' + fixtitle + '.' + row['Type'].lower()

    os.makedirs(destdir, exist_ok=True)
    shutil.copyfile(row['Path'], destdir + destfile)

