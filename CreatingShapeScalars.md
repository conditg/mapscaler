# How to Calculate Area Scalars from a variable

In this tutorial, we'll use a GeoPandas dataframe with 2 columns: a `geometry` column of US state shapes, and a `population` column of numeric values. (Of course, the following steps will work for other variables besides population - any numeric input will do.)

```python
import ms

loader = ms.MapLoader()

df = loader.fetch_states()['df']
```

## Step 1: Choose a 'base' for scale

While scalars clearly define proportions, they do not specify any sizes specifically. For example, California's populations is 20x larger than New Jersey's population. This could be satisfied by respective areas of 20 and 1, 200 and 10, 2 million and 1 million, etc. You must specificy some anchor for the overall scale of the new map.  

When you scale a shape by some scalar x, the area scales at x<sup>2</sup>. Typically when resizing shapes on a geographic map, the user's intention is to scale the area of those shapes. This can lead to confusion when the shapes scale much faster than expected. If your intention is to scale the area of a shape, pass scaler functions the square root of each coordinate scalar.  

### Additional Reading:
- [Square-cube Law](https://en.wikipedia.org/wiki/Square-cube_law)
- [Calculating the scale factor to resize a polygon to a specific size](https://math.stackexchange.com/questions/1889423/calculating-the-scale-factor-to-resize-a-polygon-to-a-specific-size)
