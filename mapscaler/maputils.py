from shapely.geometry import Point,Polygon, MultiPolygon
import pandas as pd
import numpy as np
import geopandas as gpd


def alberize(lat,
             long,
             R=1,
             std_prl_1=29.5,
             std_prl_2=45.5,
             map_centroid_lat=39.8,
             map_centroid_long=-98.5):
    '''
    Converts a (lat, long) point to its (x,y) coordinates
    in an albers equal area projection. More info on page 100:
    https://pubs.usgs.gov/pp/1395/report.pdf
    
    Inputs:
        lat: Latitude of the point to convert
        long: Longitude of the point to convert
        R: Radius of the Unit Sphere
        std_prl_1: First Standard Parallel (Latitude). 
            (See Deetz & Adams 1934)
        std_prl_2: Second Standard Parallel (Latitude)
            (See Deetz & Adams 1934)
        map_centroid_lat: Latitude Center of Map 
        map_centroid_long: Longitude Center of Map
            https://pubs.usgs.gov/unnumbered/70039437/report.pdf

    ''' 
    #Inputs as radians
    lat_rad = np.deg2rad(lat)
    long_rad = np.deg2rad(long)
    theta1 = np.deg2rad(std_prl_1)
    theta2 = np.deg2rad(std_prl_2)
    theta0 = np.deg2rad(map_centroid_lat)
    lambda0 = np.deg2rad(map_centroid_long)
    
    if abs(long - lambda0)>180:
        raise 'Not Yet Implemented to support ranges larger than half the earth. '+\
            'See https://pubs.usgs.gov/pp/1395/report.pdf'
    
    #Formula Documentation: https://pubs.usgs.gov/pp/1395/report.pdf p100
    #Specific to the map
    n = ( np.sin(theta1) + np.sin(theta2) )  /2
    C = ( np.cos(theta1) )**2 + 2*n*np.sin(theta1)
    p0 = (R * ( C - 2*n*np.sin(theta0) )**.5) / n
    
    #specific to the point
    p = (R * (C - 2*n*np.sin(lat_rad) )**.5) / n
    bigtheta = n * (long - np.rad2deg(lambda0))
    newx = p * np.sin(np.deg2rad(bigtheta))
    newy = p0 - p * np.cos(np.deg2rad(bigtheta))
    
    return newx, newy

def alberize48_shape(shape):
    '''
    Input: Shapely Polygon
    Output: Shape coordinates as projected in the default 
        albers equal area projection for the lower 48 US States
    '''
    new_coords=[]
    for long,lat in shape.exterior.coords:
        x,y = alberize(lat,long)
        new_coords.append((x,y))
    return Polygon(new_coords)

def alberize48_gdf(gdf, geo):
    new_geo = []
    for shape in gdf[geo]:
        if isinstance(shape, Polygon):
            new_shape = alberize48_shape(shape)
            new_geo.append(new_shape)
        elif isinstance(shape, MultiPolygon):
            new_polys = []
            for poly in shape.geoms:
                new_poly = alberize48_shape(poly)
                new_polys.append(new_poly)
            new_geo.append(MultiPolygon(new_polys))
    newdf = gdf.copy()
    newdf[geo] = new_geo
    newdf[geo] = newdf[geo].astype('geometry')
    return newdf
