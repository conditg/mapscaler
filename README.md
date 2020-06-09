# MapScaler
![Example visualization](/images/header.png)

Scale areas of a geopandas map by any property (such as population) - without the shapes overlapping - to create more intuitive and beautiful choropleth visualizations.


## Example Usage:
Suppose you have a GeoPandas Dataframe `df`, including a column `population_scalar` that is a float column indicating how much each sample should grow or shrink to reflect each location's respective population. The goal is for the area of each location to visually portray it's contribution to the entire map for your chosen variable (population, in this example).     
```python
import mapscaler as ms

ss = ms.ShapeScaler()
scaled_df = ss.scale_map(df, 'population_scalar')
```
The above code returns a new GeoPandas dataframe with an updated geometry column.     
More realistically, you may need to tweak a few arguments to get an ideal map, depending on your scaling inputs. See [the Basic Overview](Overview.md) for more info. (See also the note on [Creating Shape Scalars](CreatingShapeScalars.md)).    

## TODO
- Post examples of various map trainings
