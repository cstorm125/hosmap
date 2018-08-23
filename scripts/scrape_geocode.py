import re
import html
import numpy as np
import pandas as pd
import dill as pickle
from collections import Counter
from bs4 import BeautifulSoup
import urllib

DATA_PATH='../data/'
RAW_PATH = '../data/raw/
  
#utils
def location_str(i):
    l = f'{hosad.iloc[i,1]} อำเภอ{hosad.iloc[i,9].split("-")[1]} จังหวัด{hosad.iloc[i,8].split("-")[1]}'
    return(l)

hosad = pd.read_csv(f'{RAW_PATH}hospital_address.csv')
hosad['lat'] = None
hosad['lon'] = None
hosad.head()

#loop
for i in range(hosad.shape[0]):
    if i % 100 ==0: print(i)
    location = location_str(i)
    GoogleAPIKey = 'YOUR KEY HERE'
    from geopy.geocoders import GoogleV3
    geolocator = GoogleV3(api_key=GoogleAPIKey)
    result = geolocator.geocode(query=location, language='th', exactly_one=False, timeout=5)
    if result is None: 
        print(f'{i} Cannot geocode')
        lat, lon = None, None
    else:
        lat,lon = result[0][1]
    hosad.iloc[i,hosad.columns.get_loc('lat')] = lat
    hosad.iloc[i,hosad.columns.get_loc('lon')] = lon
    hosad.to_csv(f'{DATA_PATH}hospital_latlon.csv',index=False)
