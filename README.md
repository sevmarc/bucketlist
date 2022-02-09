# bucketlist
This is my interactive bucketlist

## What it contains:
- bucketlist folder  
    Contains notes created in markdown, using the [Obsidian](obsidian.md) editor.  
    PLACES have places, structured around country-level.  
    Add comment with LOC (<!--- LOC --->) before line with location name, so it is found by the parser, which then adds it on a map.
- parse_places.py  
    Python module used to 
    conda
    - Install setup:  
        `conda config --prepend channels conda-forge`  
        `conda create -n ox --strict-channel-priority osmnx`  
        `pip install geopy`  
        (in the future, a docker image may be provided for environment)
    - Activate setup:  
        `conda activate ox`  
    Just run the file, the outout will be: `bucketlist.html` containing the OSM map

# Map
See the map source [here](https://github.com/sevmarc/bucketlist/blob/main/bucketlist.html)