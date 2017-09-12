# should be at GabWork level

import pandas as pd
from sklearn.neighbors import NearestNeighbors
import json
import numpy as np
import pickle

with open('confignn.json') as f:
    confignn = json.load(f)

# config variables
ef1 = confignn["extracted_features_1"]
ef1on = confignn["feat1_on"]
ef2 = confignn["extracted_features_2"]
ef2on = confignn["feat2_on"]
ef3 = confignn["extracted_features_3"]
ef3on = confignn["feat3_on"]

dfholder = []

# get features loaded into frames
if ef1on == 1:
    df1 = pd.read_pickle(ef1)
    df1['image'] = df1['name'].apply(lambda x: x[0:-6])
    df1 = df1.drop('name', axis=1)
    df1 = df1.rename(columns={'feature': 'feat1'})
    df1 = df1.drop_duplicates(['image'], keep='last')
    dfholder.append(df1)
    filename = "nn_one"
if ef2on == 1:
    df2 = pd.read_pickle(ef2)
    df2['image'] = df2['name'].apply(lambda x: x[0:-6])
    df2 = df2.drop('name', axis=1)
    df2 = df2.rename(columns={'feature': 'feat2'})
    df2 = df2.drop_duplicates(['image'], keep='last')
    dfholder.append(df2)
    filename = "nn_two"
if ef3on == 1:
    df3 = pd.read_pickle(ef3)
    df3['image'] = df3['name'].apply(lambda x: x[0:-6])
    df3 = df3.drop('name', axis=1)
    df3 = df3.rename(columns={'feature': 'feat3'})
    df3 = df3.drop_duplicates(['image'], keep='last')
    dfholder.append(df3)
    filename = "nn_three"

if len(dfholder) == 1:
    df = dfholder[0]
    featn = df.columns[0]
    df = df.rename(columns={featn: 'features'})
elif len(dfholder) == 2:
    df = pd.merge(dfholder[0], dfholder[1], how="inner", left_on="image", right_on="image")
    f1 = df.columns[0]
    f2 = df.columns[2]
    df['features'] = df.apply(lambda row: list(row[f1]) + list(row[f2]), axis=1)
elif len(dfholder) == 3:
    df = pd.merge(dfholder[0], dfholder[1], how="inner", left_on="image", right_on="image")
    df = pd.merge(df, dfholder[2], how="inner", left_on="image", right_on="image")
    f1 = df.columns[0]
    f2 = df.columns[2]
    f3 = df.columns[3]
    df['features'] = df.apply(lambda row: list(row[f1]) + list(row[f2]) + list(row[f2]), axis=1)
else:
    print('error with amount of features on')


# run NN

x = list(df['features'])
nbrs = NearestNeighbors(n_neighbors=25, algorithm='ball_tree').fit(x)
distances, indices = nbrs.kneighbors(x)

df = df.assign(nbors=list(indices))
df = df.assign(dist=list(distances))

df['nbors_names'] = df['nbors'].apply(lambda x: [df['image'][i] for i in x])


df.to_pickle(filename + '.pkl')

output_json = {}
for idx, name in enumerate(df['image']):
    output_json[name]['neighbors'] = df['nbors_names'][idx]
    output_json[name]['distances'] = df['dist'][idx]


json = json.dumps(output_json)
f = open(filename + ".json", "w")
f.write(json)
f.close()




