# Overview of MapScaler
## The Basics
MapScaler allows you to scale the polygons in a [geopandas dataframe](https://geopandas.org/reference/geopandas.GeoDataFrame.html) by a variable, then reorganizes the newly-sized polygons to prevent overlapping. See some examples [here](https://medium.com/@conditg/map-scaler-examples-scale-any-map-by-any-variable).
After the initial scaling step, MapScaler works iteratively, gently and strategically nudging the polygons in your map until they don't overlap.
Below is a quick overview, using 4 circles to create a minimalist example.    
![Original Chart](/images/original.png)    
Suppose these circles are scaled by a variable, and as a consequence, there's some unwanted overlap:    
![Scaled Chart](/images/scaled.png)    
The first step to removing overlap is to find the centroid of the map, all shapes included:    
![Map Centroid](/images/step1.png)    
Next, organize all the shapes into groups with other shapes they overlap. Shapes that don't overlap any others do not need to be moved, so they are not members of any group.    
![Group Membership](/images/step2.png)    
Next, find the centroid of each group:    
![Group Centroids](/images/step3.png)    
The direction that each shape will move is a function of its position in relation to BOTH the map centroid, and its group centroid. The degree to which each centroid relation is considered in the formation of the direction vector is determined by the arguments `mapLR` and `groupLR`. Guidelines on using these will be posted at a later date, but in short, the group centroid should be the primary driver of the direction vector, and the map centroid should just be included minimally to achieve faster resolution in cases where a shape gets 'stuck' between 2 others.    
![Direction Vector](/images/step4.png)    
![Repeat 2-4](/images/step5.png)    

The Bubble Scaler works the same way after converting all shapes in your map to circles with the equivalent area.
