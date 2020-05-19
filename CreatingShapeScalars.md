# Creating Shape Scalars

When you scale a shape by some scalar x, the area scales at x<sup>2</sup>. Typically when resizing shapes on a geographic map, the user's intention is to scale the area of those shapes. This can lead to confusion when the shapes scale much faster than expected. If your intention is to scale the area of a shape, pass scaler functions the square root of each coordinate scalar.  

### Additional Reading:
- [Square-cube Law](https://en.wikipedia.org/wiki/Square-cube_law)
- [Calculating the scale factor to resize a polygon to a specific size](https://math.stackexchange.com/questions/1889423/calculating-the-scale-factor-to-resize-a-polygon-to-a-specific-size)
