import folium
from geopy.geocoders import Nominatim
from pathlib import Path, PosixPath


keyword = '<!--- LOC --->'  # this marks the locations in *.md files

letters = 'abcdefghijklmnopqrstuvwxyz'  # used to distinguish letters


class Location:
    def __init__(self, location_name: str, country: str):
        """
        Location name is 'cleaned up'
        Country information comes from filename ('Scotland.md', etc.)
        """
        self.location_name_raw = location_name
        self.country = country.lower()  # for simplicity, everything is lowercase
        self.location_name = self.parse_line()
        self.finalized_location = self.location_name + ', ' + self.country

        self.lat_long = None  # None, until get_geolocation is run successfully
        print(self.finalized_location)  # this is mainly for debugging

    def parse_line(self) -> str:
        """ 
        Takes a raw place input (raw line from the md document, 
        and cuts only the real geographic name from it;
        this can then be understood by the geocoder. 
        """
        location_name_raw_small = self.location_name_raw.lower()
        start_loc, end_loc = 0, 0
        looking_started = False
        for i, l in enumerate(location_name_raw_small):
            if not looking_started:
                if l in letters:
                    looking_started = True
                    start_loc = i
            else:
                if l not in (letters + ' '):
                    end_loc = i
                    break
        place = location_name_raw_small[start_loc:end_loc]

        return place

    def get_geolocation(self, nom: Nominatim):
        get_loc = nom.geocode(self.finalized_location)
        if get_loc:
            self.lat_long = [get_loc.latitude, get_loc.longitude]
            return self.lat_long
        else:  # NoneType
            print(f'\'{self.finalized_location}\' was not understood. ')


def list_filenames(main_path: str = 'bucketlist/PLACES',
                   file_extension: str = 'md') -> list[PosixPath]:
    """ Lists all files under main_path with file_extension extension """
    results = []
    for path in Path(main_path).rglob(f'*.{file_extension}'):
        results.append(path)
    return results


def parse_places() -> list[Location]:
    """ 
    Calls list_filenames, finds every location using the keyword, 
    then parses them into clean format, usable for map plotting.
    """
    places_raw = []

    for filename in list_filenames():
        with open(filename) as tf:
            lines = tf.readlines()
            filename_noext = filename.stem  # no extension

        for ind, line in enumerate(lines):
            if keyword in line:  # the next line contains location info
                places_raw.append([lines[ind + 1], filename_noext])

    return [Location(place, country) for place, country in places_raw]


def plot_location(locations: list[Location]):
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
        lat_long = location.get_geolocation(loc)
        if lat_long:
            folium.CircleMarker(location=location.lat_long).add_to(m)
    m.save('bucketlist.html')
    print(f'Bucketlist map was saved to: bucketlist.html')


if __name__ == '__main__':
    places = parse_places()
    plot_location(places)
