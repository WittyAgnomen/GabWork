import urllib.request
import pandas as pd

# load frame
df = pd.read_csv('published_assets_full_fixed.csv')

# get lists
name = list(df['assetName'])
pic = list(df['assetURL'])

i = 138430

failed = []

while i < len(name):
    try:
        urllib.request.urlretrieve(pic[i], "%s.jpg" % name[i])
        print(i)
        i += 1
    except:
        print("this one failed", "%s" % name[i])
        failed.append(name[i])
        i += 1
