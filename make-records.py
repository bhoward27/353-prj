# WARNING: This code took about 50 minutes to run on my laptop.
# I'm sure there's a way to do this the proper Pandas way, but I couldn't figure it out.

import pandas as pd
import numpy as np

def main():
    df = pd.read_json('amenities-vancouver.json.gz', lines=True)
    boundaries = pd.read_csv('boundaries.csv')

    i = 0
    n = len(df.index)
    last_percent = 0
    df['box id'] = pd.Series(dtype='int64')
    print(" Processed 0% of all records.", sep="", end="\r")
    for index_a, a in df.iterrows():
        lat = a.lat
        lon = a.lon
        for index_b, b in boundaries.iterrows():
            lat1 = b.lat1
            lat2 = b.lat2
            lon1 = b.lon1
            lon2 = b.lon2
            if (lat1 <= lat and lat < lat2) and (lon1 <= lon and lon < lon2):
                df.loc[index_a, 'box id'] = index_b
                break
        percent = ((i + 1) * 100) // n
        if (percent > last_percent):
            print(" Processed ", percent, "% of all records.", sep="", end="\r")
            last_percent = percent
        i += 1
        
    df.to_csv('records.csv')

if __name__ == "__main__":
    main()