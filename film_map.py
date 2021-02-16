import pandas as pd
import os
import geopy
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic, distance
from geopy.extra.rate_limiter import RateLimiter

def read_file(path):
    """
    """
    y = lambda x: (x[0], x[-1])
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = [y(line.strip('\n').split('\t')) for line in file]
    return lines


def sort_data(data, year, place):
    """
    """
    sorted_list = []
    for tpl in data:
        try:
            if int(tpl[0][tpl[0].find('(')+1:tpl[0].find(')')]) == year and tpl[1].find(place) != -1:
                sorted_list.append(tpl)
        except ValueError:
            continue
    return sorted_list



def input_location():
    """
    """
    lat = input("Enter the latitude: ")
    long = input("Enter the longitude: ")
    year = input("Enter the year: ")
    return lat, long, year



def map_generator(lat, long, data_list):
    """
    """
    map = folium.Map(location=[lat, long], zoom_start=10, tiles="Stamen Terrain")
    data = pd.DataFrame({
        'lat': [int(i[1][0]) for i in data_list],
        'long': [int(i[1][1]) for i in data_list],
        'name': [i[0][0] for i in data_list]
    })
    for i in range(0, len(data)):
        folium.Marker([data.iloc[i]['long'], data.iloc[i]['lat']], popup=data.iloc[i]['name']).add_to(map)
    map.save('Film_Map.html')
    return map


def closest_to_me(lat, long, data):
    """
    """

    return list(sorted(map(lambda x: [*x, find_distance(lat, long, x[1])], map(lambda x: [x[0], location_films(x[1])], data)), key=lambda x: x[-1]))[:10]



def my_location(lat, long):
    """
    """
    geolocator = Nominatim(user_agent="film_map")
    location = geolocator.reverse(f"{lat}, {long}", language="en")
    return location.address


def location_films(place):
    """
    """
    geolocator = Nominatim(user_agent="film_map")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geolocator.geocode(place,  language="en")
    return (location.latitude, location.longitude) if location is not None else (-54, -34)


def find_distance(lat, long, city):
    """
    """
    return distance((lat, long), city).km

def main():
    lat, long, year = input_location()
    factor = my_location(lat, long).split(', ')[-1]
    data = sort_data(read_file(os.path.join(os.getcwd(), 'locations.csv')), year, factor)
    map_generator(lat, long, closest_to_me(lat, long, data))



if __name__ == '__main__':
    main()
