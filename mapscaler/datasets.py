import geopandas as gpd
import os

class MapLoader():
    """Quickly load common maps of the US as GeoPandas Dataframes.
    
    .. note:: In most cases, the least detailed map options are used for performance. 
        All MapLoader methods return a ``sources`` item with links to find maps
        with higher detail, if available.  
    """
    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.USCB_paths = {'population':
          'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv',
          'geography':
          'https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html'
         }
        
    def fetch_counties(self, state_fips=None):
        '''
        Load a map of the US counties.
        
        :param state_fips: *Optional* - State FIPS code as a string. Default is ``None`` which loads all states.
        :type state_fips: str
        :returns: ``dict`` with 2 keys: 
        
            **df** is a `GeoPandas DataFrame <https://geopandas.org/reference/geopandas.GeoDataFrame.html>`_,\
                including a column of shape objects. 
                
            **sources** is a dict of links to the original map source.
        :rtype: ``dict``
        '''
        gdf = gpd.read_file(os.path.join(self.path,'geojson','us_counties.json'))
        if state_fips:
            gdf = gdf[gdf.STATE_FIPS==str(state_fips)].copy()
        return {'df':gdf, 'sources':self.USCB_paths}
    
    def fetch_states(self):
        '''
        Load a map of the US states, including Puerto Rico.
        
        :returns: ``dict`` with 2 keys: 
        
            **df** is a `GeoPandas DataFrame <https://geopandas.org/reference/geopandas.GeoDataFrame.html>`_,\
                including a column of shape objects. 
                
            **sources** is a dict of links to the original map source.
        :rtype: ``dict``
        '''
        gdf = gpd.read_file(os.path.join(self.path, 'geojson','us_states.json'))
        return {'df':gdf, 'sources':self.USCB_paths}
