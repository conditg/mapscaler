import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.ops import unary_union
from shapely.strtree import STRtree
from shapely.affinity import scale


class BaseScaler():
    def __init__(self):
        self.overlapping_groups = {}
        self.overlapping_groups_index = {}
        self.index_by_id = {}
        self.group_centroids = {}     
        
    def get_group_centroid(self, obj_list):
        '''
        Input: iterable of Shapely objects
        Output: [x,y] coordinates of the entire group's centroid
        '''
        polygon_list = []
        for shape in obj_list:
            if isinstance(shape, Polygon):
                polygon_list.append(shape)
            elif isinstance(shape, MultiPolygon):
                polygon_list = polygon_list + [poly for poly in shape.geoms]
            else:
                raise ValueError('Geometry values must be Shapely objects, not {}'.format( type(shape) ) )
        centroid = MultiPolygon(polygon_list).centroid.coords.xy
        return [coord[0] for coord in centroid]

    def get_overlapping_groups(self, df, geo, buffer):
        '''
        Input: 
            df: Geopandas df
            geo: string name of geometry column in df
            buffer: Distance required between shapes before they are considered non-overlapping
        Outputs:
            overlapping_groups: {k:v} where k is the group id and v is a list of shape ids.
        '''
        #create indices to speed up
        tree = STRtree(df[geo])
        
        overlapping_groups={}
        groups_created = 0
        for shape in df[geo]:
            in_existing=False
            #Quickly find objects which have overlapping extents
            overlaps = tree.query(shape.buffer(buffer))
            #Reduce that subset to objects which truly overlap
            overlaps = [x for x in overlaps if shape.buffer(buffer).intersects(x)]
            overlaps_ids = set([id(x) for x in overlaps])
            #Check all created groups for ANY overlap
            #while overlapping_groups to check still exist:
            current_group = groups_created
            while current_group>0:
            #If any overlapping shapes are already in the group:
                if len(overlaps_ids.intersection(overlapping_groups[current_group])):
                    for shape in overlaps:
                        #add them all to that group
                        overlapping_groups[current_group].add(id(shape))
                    in_existing=True
                    break
                else:
                    #move on to check the next group
                    current_group = current_group-1

            if not in_existing:
                if len(overlaps)==1:
                    #The shape doesn't overlap any others
                    pass
                elif len(overlaps)>1:
                    #Create a new group with this shape, and all its overlaps
                    overlapping_groups[groups_created+1] = set([id(poly) for poly in overlaps])
                    groups_created += 1

        #previously unintersecting sets can become intersecting with later additions
        #The next steps do a final confirmation of the exclusivity of all sets, merging any with common member shapes
        groupkeys = set(overlapping_groups.keys())
        for key in groupkeys:
            #check all except itself
            groups_to_check = groupkeys.copy()
            groups_to_check.remove(key)
            confirmed=False
            while not confirmed:
                for key2 in groups_to_check:
                    if (overlapping_groups[key] & overlapping_groups[key2]):
                        #If there's an overlap, set one group to a union and the other to empty
                        #no deletion while iterating over the keys of overlapping_groups
                        overlapping_groups[key] = overlapping_groups[key].union(overlapping_groups[key2])
                        overlapping_groups[key2] = set()
                        break
                #whether overlap was found or not, set is confirmed unique after checking all other groups
                confirmed=True
        #remove any  empty sets
        overlapping_groups = {k: v for k, v in overlapping_groups.items() if v}
        return overlapping_groups
    
    def index_overlapping_groups(self):
        '''
        Output: 
            overlapping_groups_index: {k,v} where k is a shape id and v is a group number.
        '''
        overlapping_groups_index = {}
        for groupnum, members in self.overlapping_groups.items():
            for member_id in members:
                overlapping_groups_index[member_id] = groupnum
        return overlapping_groups_index
    
    
    def update_group_centroids(self, df, geo):
        '''
        Inputs:
            df: Geopandas dataframe
            geo: string name of geometry column in df
        Output:
            group_centroids: {k,v} where k is the group id and v is the group centroid.
        '''    
        group_centroids = {}
        for groupnum, members in self.overlapping_groups.items():
            #for each group:
            shape_list = []
            for member_id in members:
                #append each group member to the shape list
                shape_list.append(df[geo][self.index_by_id[member_id]])
            #find centroid of the group
            group_centroids[groupnum] = self.get_group_centroid(shape_list)
        group_centroids['all'] = self.get_group_centroid(df[geo])
        return group_centroids       

    def index_geo_col(self, df, geo):
        '''
        Inputs:
            df: Geopandas dataframe
            geo: string name of geometry column in df
        Output:
            index_by_id: {k,v} where k is a shape id, and v is its row index in the df.
        '''
        index_by_id = dict((id(poly), i) for i, poly in enumerate(df[geo]))
        return index_by_id
    
    def move_shape(self, shape, movement):
        '''
        Input: shapely Polygon, and a movement vector [x,y]
        Output: shapely Polygon with coordinates moved by the movement vector
        '''
        new_longs = []
        new_lats = []
        for long, lat in shape.exterior.coords:
            new_long = long + movement[0]
            new_lat = lat + movement[1]
            new_longs.append(new_long)
            new_lats.append(new_lat)
        new_shape = Polygon(zip(new_longs, new_lats))
        return new_shape

    def nudge_shapes(self, df, geo, map_vel, group_vel):
        '''
        Nudges overlapping shapes away from group and map centroids.
        Inputs:
            df: Geopandas dataframe
            geo: string name of geometry column in df
            map_vel: Velocity at which shapes are nudged away from the whole map's centroid
            group_vel: Velocity at which shapes are nudged away from their group's centroid
        
        Outputs: Geopandas Dataframe with updated geometry column
        '''
        new_shapes = []
        for shape in df[geo]:
            if id(shape) in list(self.overlapping_groups_index.keys()):
                #If the shape overlaps any others:
                group = self.overlapping_groups_index[id(shape)]
                centroid = [coord[0] for coord in list(shape.centroid.coords.xy)]
                groupcentroid = self.group_centroids[group]
                #calculate the direction vectors from the map and group centroids
                mapnudge = [shape_coord - map_coord for shape_coord, map_coord in zip(centroid, self.group_centroids['all'])]
                groupnudge = [shape_coord - group_coord for shape_coord, group_coord in zip(centroid, groupcentroid)]
                #Create a movement vector by scaling the two direction vectors by velocity and summing
                movement = [(map_vec*map_vel + group_vec*group_vel) for map_vec,group_vec in zip(mapnudge, groupnudge)]
                #Move the shape by the movement vector
                if isinstance(shape,Polygon):
                    shape = self.move_shape(shape,movement)
                elif isinstance(shape,MultiPolygon):
                    poly_list = []
                    for part in shape.geoms:
                        poly = self.move_shape(part, movement)
                        poly_list.append(poly)
                    shape = MultiPolygon(poly_list)
                else:
                    raise ValueError('Geometry values must be Shapely objects, not {}'.format( type(shape) ) )
            new_shapes.append(shape)
        dfnew = df.copy()
        dfnew[geo] = new_shapes
        return dfnew


    def separate_map(self, df, geo, map_vel, group_vel, buffer, max_iter, verbose):
        '''
        Inputs:
            df: Geopandas dataframe
            geo: string name of geometry column in df
            map_vel: Velocity at which shapes are moved away from the whole map's centroid
            group_vel: Velocity at which shapes are moved away from their group's centroid
            buffer: Distance required between shapes before they are considered non-overlapping
            max_iter: Maximum number of attempts to resolve overlaps by nudging shapes
            verbose: boolean - prints progress as shapes are separated
        
        Outputs: 
            Geopandas df with updated geometry column
        '''
        newdf = df.copy()
        for i in range(max_iter):
            if verbose:
                print('Iteration {}'.format(i+1) )
            #index the new dataframe
            self.index_by_id = self.index_geo_col(newdf, geo)
            #Identify and index overlapping groups
            self.overlapping_groups = self.get_overlapping_groups(newdf, geo, buffer)
            self.overlapping_groups_index = self.index_overlapping_groups()
            #Store centroid of each group
            self.group_centroids = self.update_group_centroids(newdf, geo)
            if self.overlapping_groups:
                newdf = self.nudge_shapes(newdf,geo, map_vel, group_vel)
                if verbose:
                    print('--{} overlapping groups remaining'.format( len(self.overlapping_groups) ) )
            else:
                if verbose:
                    print('Separated in {} iterations'.format(i+1) )
                break
                
        return newdf
    
    def get_group_members(self, original_df, property_col):
        '''
        Prints the members of each group, given a column from the
        original dataframe to print. Useful for debugging groups that won't converge.
        
        Inputs: 
            original_df: GeoPandas Dataframe previously passed to scale_map method.
            property_col: String name of column in original_df that identifies each shape. Typically
                a name or ID.
        '''
        group_members = {}
        for groupnum, members in self.overlapping_groups.items():
            group_members[groupnum] = []
            for member_id in members:
                group_members[groupnum].append(original_df[property_col][self.index_by_id[member_id]])
        return group_members
    
    
class ShapeScaler(BaseScaler):
    
    def scale_shapes(self, df, scaleby, geo):
        '''
        Input: Geopandas df, string name of column with scale values
        Output: Geopandas df with updated geometry column
        
        NOTE: This function scales by coordinates. Scaling coordinates by x will
        scale the area of the shape by x^2. More info:
        https://github.com/conditg/map-scaler/blob/master/CreatingShapeScalars.md
        '''
        newShapes = []
        for shape, scaleby in zip(df[geo], df[scaleby]):
            poly = scale(shape, xfact=scaleby,yfact=scaleby,origin='center')
            newShapes.append(poly)
        newdf = df.copy()
        newdf[geo] = newShapes
        newdf[geo] = newdf[geo].astype('geometry')
        return newdf   
    
    def scale_map(self, df, scale_by, geo='geometry', map_vel=.01, group_vel=.1, buffer=0, max_iter=100, verbose=False):
        '''
        Inputs:
        df: Geopandas dataframe
        scale_by:string name of scalar column in df
        geo: string name of geometry column in df
        map_vel: Velocity at which shapes are moved away from the whole map's centroid
        group_vel: Velocity at which shapes are moved away from their group's centroid
        buffer: Space required between shapes before they are considered non-overlapping
        max_iter: Maximum number of attempts to nudge shapes away from each other
        verbose: boolean - prints progress as shapes are separated

        Outputs: Geopandas df with updated geometry column
        '''
        scaled_df = self.scale_shapes(df, scale_by, geo)
        separated_df = self.separate_map(scaled_df, geo, map_vel, group_vel, buffer, max_iter, verbose)
        return separated_df
    
    
    
class BubbleScaler(BaseScaler):
    
    def scale_bubbles(self, df, scaleby, geo):
        '''
        Input: Geopandas df, string name of column with scale values
        Output: Geopandas df with updated geometry column, each shape converted to a same-area circle 
        
        NOTE: This function scales by coordinates. Scaling coordinates by x will
        scale the area of the circle by x^2. More info:
        https://github.com/conditg/map-scaler/blob/master/CreatingShapeScalars.md
        '''
        bubbles = []
        for shape, scaleby in zip(df[geo], df[scaleby]):
            area = shape.area
            long,lat = shape.centroid.coords.xy
            unscaled_bubble = Point(long[0],lat[0]).buffer(np.sqrt(area/np.pi), resolution=70)
            bubble = scale(unscaled_bubble, xfact=scaleby,yfact=scaleby,origin='center')
            bubbles.append(bubble)
        newdf = df.copy()
        newdf[geo] = bubbles
        newdf[geo] = newdf[geo].astype('geometry')
        return newdf   
    
    def scale_map(self, df, scale_by, geo='geometry', map_vel=.01, group_vel=.1, buffer=0, max_iter=100, verbose=False):
        '''
        Inputs:
        df: Geopandas dataframe
        scale_by:string name of scalar column in df
        geo: string name of geometry column in df
        map_vel: Velocity at which shapes are moved away from the whole map's centroid
        group_vel: Velocity at which shapes are moved away from their group's centroid
        buffer: Space required between shapes before they are considered non-overlapping
        max_iter: Maximum number of attempts to nudge shapes away from each other
        verbose: boolean - prints progress as shapes are separated

        Outputs: Geopandas df with updated geometry column
        '''
        bubbled_df = self.scale_bubbles(df, scale_by, geo)
        separated_df = self.separate_map(bubbled_df, geo, map_vel, group_vel, buffer, max_iter, verbose)
        return separated_df