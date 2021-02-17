"""Film map"""

import os
import folium
from geopy.geocoders import Nominatim
from geopy.distance import distance
from geopy.extra.rate_limiter import RateLimiter

def read_file(path):
    """
    Reads file
    """
    y = lambda x: (x[0], x[-1])
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = [y(line.strip('\n').split('\t')) for line in file]
    return lines


def sort_data(data, year, place):
    """
    Sorts the data
    """
    sorted_list = []
    name_dict = {"United States": "USA"}
    for tpl in data:
        try:
            if int(tpl[0][tpl[0].find('(')+1:tpl[0].find(')')]) == year and tpl[1].find(name_dict.get(place, place)) != -1:
                sorted_list.append(tpl)
        except ValueError:
            continue
    return sorted_list



def input_location():
    """
    Inputs location
    """
    lat = int(input("Enter the latitude: "))
    long = int(input("Enter the longitude: "))
    year = int(input("Enter the year: "))
    return lat, long, year



def map_generator(lat, long, data_list):
    """
    Generates html file with the map
    """
    map = folium.Map(location=[lat, long], zoom_start=6, tiles="Stamen Terrain")
    for name, coord, _ in data_list:
        folium.Marker([coord[0], coord[1]], popup=name).add_to(map)
    map.save('Film_Map.html')
    return map


def closest_to_me(lat, long, data):
    """
    Finds 10 closest film shooting location
    """
    return list(sorted(map(lambda x: [*x, find_distance(lat, long, x[1])], map(lambda x: [x[0], location_films(x[1])], data)), key=lambda x: x[-1]))[:10]



def my_location(lat, long):
    """
    Finds location address
    """
    geolocator = Nominatim(user_agent="film_map")
    location = geolocator.reverse(f"{lat}, {long}", language="en")
    return location.address


def location_films(place):
    """
    Finds location of films shooting places
    """
    geolocator = Nominatim(user_agent="film_map")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geolocator.geocode(place,  language="en")
    return (location.latitude, location.longitude) if location is not None else (-54, -34)


def find_distance(lat, long, city):
    """
    Finds distance between two points
    """
    return distance((lat, long), city).km

def main():
    """
    Main function
    """
    lat, long, year = input_location()
    factor = my_location(lat, long).split(', ')[-1]
    path = os.path.join(os.getcwd(),'Task-2', 'locations.csv')
    data = sort_data(read_file(path), year, factor)
    map_generator(lat, long, closest_to_me(lat, long, data))



if __name__ == '__main__':
    main()
