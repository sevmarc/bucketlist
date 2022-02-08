import osmnx as ox
import folium
from geopy.geocoders import Nominatim


target_file = "bucketlist/PLACES/EUROPE/Scotland.md"

keyword = '<!--- LOC --->'

letters = 'abcdefghijklmnopqrstuvwxyz'


def parse_places(filename: str=target_file) -> list[str]:
    places_raw = []
    
    with open(target_file) as tf:
        lines = tf.readlines()
    
    for ind, line in enumerate(lines):
        if keyword in line:
            places_raw.append(lines[ind + 1])
    
    return [parse_line(place) for place in places_raw]


def parse_line(place_raw: str) -> str:
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
    # print(place)
    return place

def plot_location(locations: list[str]):
    loc = Nominatim(user_agent="getLoc")
    
    origo = loc.geocode('Budapest, Hungary')
    orig_xy = [origo.latitude, origo.longitude]
    m = folium.Map(orig_xy, zoom_start=3)

    for location in locations:
        getLoc = loc.geocode(location)
        folium.CircleMarker(location=[getLoc.latitude, getLoc.longitude]).add_to(m)
    m.save('bucketlist.html')


if __name__ == '__main__':
    places = parse_places()
    plot_location(places)