#This program produces a json file (restaurantsByCity.json) that has the city each data point is in!
#Uses Nominatim to look up the city a set of coordinates is in
#It takes FOREVER, by the way

import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="braedenm@sfu.ca")
#user_agent must be any valid email

def getCity(row):
    try:
        location = geolocator.reverse(row["coordinates"]).raw
        return location["address"]["city"]
    except KeyError:
        return "NONE"

#This function (inconsistently) retrieves the neighbourhood for certain data points
#Very few neighbourhoods are actually retrieved by this, so it is basically useless
def getNeighbourhood(row):
    try:
        location = geolocator.reverse(row["coordinates"]).raw
        return location["address"]["suburb"]
    except KeyError:
        return "NONE"
    
def getCoordinateString(row):
    return str(row["lat"]) + "," + str(row["lon"])

data = pd.read_json("amenities-vancouver.json", lines=True)
data = data.drop(['timestamp'], axis = 1)
data = data.dropna()
data = data[(data['amenity'] == 'pub') | (data['amenity'] == 'bar') | (data['amenity'] == 'restaurant') | (data['amenity'] == 'fast_food') | (data['amenity'] == 'cafe')]
data = data.drop(['tags'], axis = 1)

data["coordinates"] = data.apply(lambda row: getCoordinateString(row), axis=1)
#data["neighbourhood"] = data.apply(lambda row: getNeighbourhood(row), axis=1)
data["city"] = data.apply(lambda row: getCity(row), axis=1)
print("Done API calls!")
jsonData = data.to_json('restaurantsByCity.json', orient='index')
print("Done writing to JSON!")
