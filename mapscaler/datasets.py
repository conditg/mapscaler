import geopandas as gpd
import os

class MapLoader():
    
    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.USCB_paths = {'population':
          'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv',
          'geography':
          'https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html'
                         }
        
    def fetch_counties(self, state_fips=None):
        gdf = gpd.read_file(os.path.join(self.path,'geojson','us_counties.json'))
        if state_fips:
            gdf = gdf[gdf.STATE_FIPS==str(state_fips)].copy()
        return {'df':gdf, 'sources':self.USCB_paths}
    
    def fetch_states(self):
        gdf = gpd.read_file(os.path.join(self.path, 'geojson','us_states.json'))
        return {'df':gdf, 'sources':self.USCB_paths}
