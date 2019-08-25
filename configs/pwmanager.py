#!/home/infrared/anaconda3/bin/python
import pandas as pd

pws = pd.read_csv("/tmp/pw.csv")

choice = input("Password? > ")

if choice.lower() == "all":
    print(pws)
else:
    print(pws[pws['name'].str.lower() == choice])
