import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely.strtree import STRtree
from shapely.affinity import scale
import math

def get_group_centroid(obj_list):
    '''
    Input: iterable of Shapely objects
    Output: [x,y] coordinates of the group's centroid
    '''
    polygon_list = []
    for shape in obj_list:
        if isinstance(shape, Polygon):
            polygon_list.append(shape)
        elif isinstance(shape, MultiPolygon):
            polygon_list = polygon_list + [poly for poly in shape.geoms]
    centroid = MultiPolygon(polygon_list).centroid.coords.xy
    return [coord[0] for coord in centroid]
    
    
def scale_geo_columns(df, scaleby, geo):
    '''
    Input: Geopandas df, column with scale values
    Output: Geopandas df with updated geometry column
    '''
    newShapes = []
    for shape, scaleby in zip(df[geo], df[scaleby]):
      poly = scale(shape, xfact=scaleby,yfact=scaleby,origin='center')
      newShapes.append(poly)
    newdf = df.copy()
    newdf[geo] = newShapes
    newdf[geo] = newdf[geo].astype('geometry')
    return newdf
    
def get_overlapping_groups(df):
    '''
    Input: Geopandas df
    Output: multiple........
    '''
    #create indices to speed up
    tree = STRtree(df['geometry'])
    index_by_id = dict((id(poly), i) for i, poly in enumerate(df['geometry']))
    
    groups={}
    n=1
    for shape in df['geometry']:
        in_existing=False
        #Quickly find objects which have overlapping extents
        overlaps = tree.query(shape.buffer(.1))
        #Reduce that subset to objects which truly overlap
        overlaps = [x for x in overlaps if shape.buffer(.1).intersects(x)]
        overlaps_ids = set([id(x) for x in overlaps])
      
        #while groups to check still exist:
        groupnum = n-1
        while groupnum>1:
        #If any overlapping shapes are already in the group:
            if len(overlaps_ids.intersection(groups[groupnum])):
                for s in overlaps:
                    #add them all to that group
                    groups[groupnum].add(id(s))
                in_existing=True
                break
            else:
                #check the next group
                groupnum = groupnum-1
            
        if not in_existing:
            if len(overlaps)==1:
                #The shape doesn't overlap any others
                pass
            elif len(overlaps)>1:
                #Create a new group with this shape, and all its overlaps
                groups[n] = set([id(poly) for poly in overlaps])
                #print('--- added to group with:')
                #print(f"---{[dfscaled['NAME_x'][index_by_id[id(x)]] for x in overlaps]}")######make a function for this? verbosity?
                n+=1

    #previously unintersecting sets can become intersecting with later additions
    #The next steps do a final confirmation of the exclusivity of all sets, merging any with common member shapes
    gkeys = set(groups.keys())
    for key in gkeys:
        #check all except itself
        groups_to_check = gkeys.copy()
        groups_to_check.remove(key)
        confirmed=False
        while not confirmed:
            for key2 in groups_to_check:
                if (groups[key] & groups[key2]):
                    #If there's an overlap, set one group to a union and the other to empty
                    #no deletion while iterating over the keys of groups
                    groups[key] = groups[key].union(groups[key2])
                    groups[key2] = set()
                    break
            confirmed=True
    #remove any  empty sets
    groups = {k: v for k, v in groups.items() if v}

    # for i in groups.keys():
    #   print(f'group {i}')
    #   print(f"---{[df['NAME_x'][index_by_id[x]] for x in list(groups[i])]}")

    #find centroids of each group DRY this up #########################################
    groupcoords = {}
    for k,v in groups.items():
        shape_list = []
        for id_ in v:
            shape_list.append(df['geometry'][index_by_id[id_]])
        groupcoords[k] = get_group_centroid(shape_list)
    groupcoords['all'] = get_group_centroid(df['geometry'])

    groups_index = {}
    for g, ids in groups.items():
        for id_ in ids:
            groups_index[id_] = g
    return groups, groupcoords, groups_index, index_by_id


def movePoly(shape, movement):
    newlong_list = []
    newlat_list = []
    for long, lat in shape.exterior.coords:
        newlong = long + movement[0]
        newlat = lat + movement[1]
        newlong_list.append(newlong)
        newlat_list.append(newlat)
    newpoly = Polygon(zip(newlong_list, newlat_list))
    return newpoly


def nudge_shapes(df,mapLR, groupLR, groupcoords, groups_index, index_by_id):
    newShapes = []
    for shape in df['geometry']:
        if id(shape) in list(groups_index.keys()):
            group = groups_index[id(shape)]
            centroid = [x[0] for x in list(shape.centroid.coords.xy)]
            groupcentroid = groupcoords[group]
            mapnudge = [a_i - b_i for a_i, b_i in zip(centroid, groupcoords['all'])]
            groupnudge = [a_i - b_i for a_i, b_i in zip(centroid, groupcentroid)]
            movement = [(a*mapLR + b*groupLR) for a,b in zip(mapnudge, groupnudge)]
            #name = dfscaled['NAME_x'][index_by_id[id(shape)]]
            if isinstance(shape,Polygon):
                shape = movePoly(shape,movement)
            elif isinstance(shape,MultiPolygon):
                mplist = []
                for part in shape.geoms:
                    poly = movePoly(part, movement)
                    mplist.append(poly)
                shape = MultiPolygon(mplist)
            else:
                raise
        newShapes.append(shape)
    dfnew = df.copy()
    dfnew['geometry'] = newShapes
    return dfnew
    
    
def separate_map(df, mapLR, groupLR, max_epochs, geo='geometry'):
    newdf = df.copy()
    for i in range(max_epochs):
        if (not i) or (groups):
            groups, groupcoords, groups_index, index_by_id = get_overlapping_groups(newdf)
            newdf = nudge_shapes(newdf, mapLR, groupLR, groupcoords, groups_index, index_by_id)
    return newdf
    
def scale_map(df, scaleby, geo='geometry', mapLR=.01, groupLR=.1, max_epochs=100):
    scaleddf = scale_geo_columns(df, scaleby, geo)
    separateddf = separate_map(scaleddf, mapLR, groupLR, max_epochs, geo)
    return separateddf