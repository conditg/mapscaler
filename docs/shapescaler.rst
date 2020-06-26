.. _ss:

Shape Scaler
=================

Simple Example
^^^^^^^^^^^^^^^^

.. image:: ../images/ssdemo.png
    :align: center

NOTE: This example uses the variable ``df`` as seen in the example in :ref:`lcm`.
::

    import mapscaler as ms

    ss = ms.ShapeScaler()
    scaled_df = ss.scale_map(df, 'scaleby', map_vel=.001, group_vel=.15, verbose=True)

If ``verbose``, :func:`~mapscaler.ShapeScaler.scale_map` will print progress as it goes (truncated below):

.. code-block:: none

    Iteration 1
    --73 overlapping groups remaining
    Iteration 2
    --79 overlapping groups remaining
    ...
    [truncated]
    ...
    Iteration 62
    --2 overlapping groups remaining
    Iteration 63
    --1 overlapping groups remaining
    Iteration 64
    Separated in 64 iterations 

Now, let's visualize the output, ``scaled_df``:
::

    import matplotlib.pyplot as plt
    import geoplot as gplt
    import numpy as np
    
    gplt.choropleth(
        df, hue=[np.log(x) for x in df.EST_POP_2019],
        projection=gplt.crs.AlbersEqualArea(), cmap='viridis',
        figsize=(15,8),
    )
    plt.title('BEFORE', fontsize=30, loc='left')
    plt.show()      

    gplt.choropleth(
        scaled_df, hue=[np.log(x) for x in df.EST_POP_2019],
        projection=gplt.crs.AlbersEqualArea(), cmap='viridis',
        figsize=(15,8),
    )
    plt.title('AFTER', fontsize=30, loc='left')
    plt.show()


Documentation
^^^^^^^^^^^^^^
.. currentmodule:: mapscaler
.. autoclass:: ShapeScaler
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
