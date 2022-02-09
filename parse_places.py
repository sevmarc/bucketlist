import osmnx as ox
import folium
from geopy.geocoders import Nominatim
import glob, os
from pathlib import Path, PosixPath


keyword = '<!--- LOC --->'  # this marks the locations in *.md files

letters = 'abcdefghijklmnopqrstuvwxyz'  # used to distinguish letters


def list_filenames(main_path: str='bucketlist/PLACES', file_extension: str='md') -> list[PosixPath]:
    """ Lists all files under main_path with file_extension extension """
    results = []
    for path in Path(main_path).rglob(f'*.{file_extension}'):
        results.append(path)
    return results

def parse_places() -> list[str]:
    """ 
    Calls list_filenames, finds every location using the keyword, 
    then parses them into clean format, usable for map plotting.
    """
    places_raw = []
    
    for filename in list_filenames():
        with open(filename) as tf:
            lines = tf.readlines()
        
        for ind, line in enumerate(lines):
            if keyword in line:
                places_raw.append(lines[ind + 1])
    
    return [parse_line(place) for place in places_raw]


def parse_line(place_raw: str) -> str:
    """ 
    Takes a raw place input (raw line from the md document, 
    and cuts only the real geographic name from it;
    this can then be understood by the geocoder. 
    """
    place_raw_small = place_raw.lower()
    start_loc, end_loc = 0, 0
    looking_started = False
    for i,l in enumerate(place_raw_small):
        if not looking_started:
            if l in letters:
                looking_started = True
                start_loc = i
        else:
            if l not in (letters + ' '):
                end_loc = i
                break 
    place = place_raw_small[start_loc:end_loc]
    
    return place


def plot_location(locations: list[str]):
    """
    Creates a map around origo;
    adds any location that was passed as a marker.
    In the future, the marker color could represent
    whether the location has been visited or not.
    
    TODO: exception handling for when the location 
    name is not understood, some sort of warning 
    should be presented to the user (me)
    """
    loc = Nominatim(user_agent="getLoc")
    
    # creating map, around origo, zoom can be reconfigured
    origo = loc.geocode('Budapest, Hungary')
    orig_xy = [origo.latitude, origo.longitude]
    m = folium.Map(orig_xy, zoom_start=3)

    for location in locations:
        get_loc = loc.geocode(location)
        folium.CircleMarker(location=[get_loc.latitude, get_loc.longitude]).add_to(m)
    m.save('bucketlist.html')


if __name__ == '__main__':
    places = parse_places()
    plot_location(places)
