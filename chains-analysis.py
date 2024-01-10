import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import math
from scipy import stats


def num_within_1km(val, df, lat_lon):
    if lat_lon == 'lat':
        lat2km = 1/111.2
        minval = val - lat2km # degree of lat in 1 km
        maxval = val + lat2km
    elif lat_lon == 'lon':
        to_radians = math.pi/180
        # Convert degree of lon to 1km
        lon2km = to_radians * 6371.0088 * np.cos(to_radians * df['lat'])
        minval = val - 1/lon2km 
        maxval = val + 1/lon2km
    num = df[(df[lat_lon] >= minval) & (df[lat_lon] <= maxval)]
    return num.shape[0]
    
def main(in_directory, out_directory):
    # Load into dataframes
    chains = pd.read_csv('chain_restaurants.csv')
    nonchains = pd.read_csv('non_chain_restaurants.csv')
    
    # Get the count for the 1km diameter at each lat and lon
    chains['lat_count'] = chains['lat'].apply(num_within_1km, args = (chains, 'lat'))
    chains['lon_count'] = chains['lon'].apply(num_within_1km, args = (chains, 'lon'))
    
    # Sort lat and lon by ascending
    lat_sorted = chains.sort_values(by = ['lat'])
    lon_sorted = chains.sort_values(by = ['lon'])
    lat_sorted['local_max'] = lat_sorted.lat[(lat_sorted.lat.shift(1) < lat_sorted.lat) & (lat_sorted.lat.shift(-1) < lat_sorted.lat)]
    lon_sorted['local_max'] = lon_sorted.lon[(lon_sorted.lon.shift(1) < lon_sorted.lon) & (lon_sorted.lon.shift(-1) < lon_sorted.lon)]
    
    # Get the max and min count of both lat and lon
    lat_count_sorted = chains.sort_values(by = ['lat_count'], ascending = False)
    lon_count_sorted = chains.sort_values(by = ['lon_count'], ascending = False)
    max_lat_loc = lat_count_sorted['lat'][lat_count_sorted.index[0]]
    min_lat_loc = lat_count_sorted['lat'][lat_count_sorted.index[-1]]
    max_lon_loc = lon_count_sorted['lon'][lon_count_sorted.index[0]]
    min_lon_loc = lon_count_sorted['lon'][lon_count_sorted.index[-1]]
    
    # Find best fit line of lat values and lon values
    lat_bfl = stats.linregress(lat_sorted['lat'].values, lat_sorted['lat_count'].values)
    lon_bfl = stats.linregress(lon_sorted['lon'].values, lon_sorted['lon_count'].values)

    # Get p-value of linear regression
    lat_pval = lat_bfl.pvalue
    lon_pval = lon_bfl.pvalue

    # Plot the number of chain restaurants within 1 km near the latitude
    plt.figure("chain_lat")
    plt.plot(lat_sorted['lat'].values, lat_sorted['lat_count'].values)
    plt.plot(lat_sorted['lat'].values, lat_bfl.slope * lat_sorted['lat'].values + lat_bfl.intercept)
    plt.title('Number of chain restaurants within 1 km near the latitude')
    plt.xlabel('Latitude')
    plt.ylabel('Number of chain restaurants')
    plt.figtext(0.5, 0.01, "p-value: " + str(lat_pval) + "\nmax count location: " + str(max_lat_loc) + "\nmin count location: " + str(min_lat_loc), ha="center")
    
    # Plot the number of chain restaurants within 1 km near the longitude
    plt.figure("chain_lon")
    plt.plot(lon_sorted['lon'].values, lon_sorted['lon_count'].values)
    plt.plot(lon_sorted['lon'].values, lon_bfl.slope * lon_sorted['lon'].values + lon_bfl.intercept)
    plt.title('Number of chain restaurants within 1 km near the longitude')
    plt.xlabel('Longitude')
    plt.ylabel('Number of chain restaurants')
    plt.figtext(0.5, 0.01, "p-value: " + str(lon_pval) + "\nmax count location: " + str(max_lon_loc) + "\nmin count location: " + str(min_lon_loc), ha="center")
    
    # Repeat for non-chain restaurants 
    nonchains['lat_count'] = nonchains['lat'].apply(num_within_1km, args = (nonchains, 'lat'))
    nonchains['lon_count'] = nonchains['lon'].apply(num_within_1km, args = (nonchains, 'lon'))
    
    lat_sorted2 = nonchains.sort_values(by = ['lat'])
    lon_sorted2 = nonchains.sort_values(by = ['lon'])
    
    lat_count_sorted2 = nonchains.sort_values(by = ['lat_count'], ascending = False)
    lon_count_sorted2 = nonchains.sort_values(by = ['lon_count'], ascending = False)
    max_lat_loc2 = lat_count_sorted2['lat'][lat_count_sorted2.index[0]]
    min_lat_loc2 = lat_count_sorted2['lat'][lat_count_sorted2.index[-1]]
    max_lon_loc2 = lon_count_sorted2['lon'][lon_count_sorted2.index[0]]
    min_lon_loc2 = lon_count_sorted2['lon'][lon_count_sorted2.index[-1]]
    
    lat_bfl2 = stats.linregress(lat_sorted2['lat'].values, lat_sorted2['lat_count'].values)
    lon_bfl2 = stats.linregress(lon_sorted2['lon'].values, lon_sorted2['lon_count'].values)

    lat_pval2 = lat_bfl2.pvalue
    lon_pval2 = lon_bfl2.pvalue

    # Plot the number of non-chain restaurants within 1 km near the latitude
    plt.figure("nonchain_lat")
    plt.plot(lat_sorted2['lat'].values, lat_sorted2['lat_count'].values)
    plt.plot(lat_sorted2['lat'].values, lat_bfl2.slope * lat_sorted2['lat'].values + lat_bfl2.intercept)
    plt.title('Number of non-chain restaurants within 1 km near the latitude')
    plt.xlabel('Latitude')
    plt.ylabel('Number of non-chain restaurants')
    plt.figtext(0.5, 0.01, "p-value: " + str(lat_pval2) + "\nmax count location: " + str(max_lat_loc2) + "\nmin count location: " + str(min_lat_loc2), ha="center")
    
    # Plot the number of non-chain restaurants within 1 km near the longitude
    plt.figure("nonchain_lon")
    plt.plot(lon_sorted2['lon'].values, lon_sorted2['lon_count'].values)
    plt.plot(lon_sorted2['lon'].values, lon_bfl2.slope * lon_sorted2['lon'].values + lon_bfl2.intercept)
    plt.title('Number of non-chain restaurants within 1 km near the longitude')
    plt.xlabel('Longitude')
    plt.ylabel('Number of non-chain restaurants')
    plt.figtext(0.5, 0.01, "p-value: " + str(lon_pval2) + "\nmax count location: " + str(max_lon_loc2) + "\nmin count location: " + str(min_lon_loc2), ha="center")
    
    plt.show()
    
    
    
if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)