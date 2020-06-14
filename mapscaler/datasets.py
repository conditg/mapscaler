import geopandas as gpd
import json
import os
class MapLoader():
    
    def __init__(self):
        self.path = 'geojson/'
        self.USCB_path = 'https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html'
    
    def fetch_counties(self, state_fips=None):
        gdf = gpd.read_file(self.path + 'us_counties.json')
        if state_fips:
            gdf = gdf[gdf.STATE==state_fips].copy()
        return {'df':gdf, 'source':self.USCB_path}
    
    def fetch_states(self):
        print(self.path + 'us_states.json')
        gdf = gpd.read_file(self.path + 'us_states.json')
        return {'df':gdf, 'source':self.USCB_path}
