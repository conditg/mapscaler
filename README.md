# MapScaler
![Example visualization](/images/header.png)

Scale geopandas shapes by any property (such as population) without the shapes overlapping


## Example Usage:
Suppose you have a GeoPandas Dataframe `df`, including a column `population_scalar` that is a float column indicating how much each sample should grow or shrink to reflect respective population.     
```python
scaled_df = scale_map(df, 'population_scalar')
```
The above code returns a new GeoPandas dataframe with and update map.     
More realistically, you may need to tweak a few arguments to get an ideal graph. See [](Overview.md) for more info.      

## TODO
- Convert to class and add a bubbling method
- Post examples of various map trainings
