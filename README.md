# MapScaler
![Example visualization](/images/header.png)

Scale geopandas shapes by any property (such as population) - without the shapes overlapping - to create more intuitive and beautiful choropleth visualizations.


## Example Usage:
Suppose you have a GeoPandas Dataframe `df`, including a column `population_scalar` that is a float column indicating how much each sample should grow or shrink to reflect each location's respective population (See also the note on [Creating Shape Scalars](CreatingShapeScalars.md). The goal is for the area of each location to visually portray it's contribution to the entire map for your chosen variable (population, in this example).     
```python
scaled_df = scale_map(df, 'population_scalar')
```
The above code returns a new GeoPandas dataframe with an updated geometry column.     
More realistically, you may need to tweak a few arguments to get an ideal map, depending on your scaling inputs. See [the Basic Overview](Overview.md) for more info.      

## TODO
- Convert to class and add a bubbling method
- Post examples of various map trainings
