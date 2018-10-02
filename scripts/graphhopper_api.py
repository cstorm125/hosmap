import numpy as np
import pandas as pd
import requests
import json
from tqdm import trange

DATA_PATH = 'data/'
RAW_PATH = f'{DATA_PATH}raw/'

api_df = pd.read_csv(f'{DATA_PATH}api_keys.csv')
api_keys = list(api_df['key'])

nearest_hoses = pd.read_csv(f'{RAW_PATH}nearest_hos.csv', sep='\t', chunksize=14000)

i=0
for nearest_hos in nearest_hoses:
    if i < 36: 
        i+=1
        continue #skip what's already done
    if i > 41: 
        print('Loop done')
        break
    api_key = api_keys[i % 5]
    nearest_hos['distance'] = None
    nearest_hos['time'] = None
    print(f'Start chunk {i}')
    for k in trange(nearest_hos.shape[0]):
        lat, lon = round(nearest_hos.iloc[k,:]['lat'], 6), round(nearest_hos.iloc[k,:]['lon'],6)
        hos_lat, hos_lon = round(nearest_hos.iloc[k,:]['hos_lat'],6), round(nearest_hos.iloc[k,:]['hos_lon'],6)
        url = f'https://graphhopper.com/api/1/route?point={lat},{lon}&point={hos_lat},{hos_lon}&vehicle=car&key={api_key}'
        r = requests.get(url)
        #time in ms and distance in m
        j = json.loads(r.text)
#         print(j)
        try:
            #convert to minutes and km
            nearest_hos.iloc[k,nearest_hos.columns.get_loc('distance')]= j['paths'][0]['distance'] / 1000
            nearest_hos.iloc[k,nearest_hos.columns.get_loc('time')] =  j['paths'][0]['time'] / 1000 / 60
        except:
            print('Invalid Point')
        if k % 1000 == 0:
            print(f'Waypoint Chunk {i} Entry {k}')
            nearest_hos.to_csv(f'{DATA_PATH}route_hos_{i}.csv',index=False)
    
    nearest_hos.to_csv(f'{DATA_PATH}route_hos_{i}.csv',index=False)
    print(f'Saved chunk {i}')
    i+=1
        
