.. _bs:

Bubble Scaler
==============

Simple Example
^^^^^^^^^^^^^^^^

.. image:: ../images/bsdemo.png
    :align: center

NOTE: This example uses the variable ``df`` as seen in the example in :ref:`lcm`.
::

    import mapscaler as ms
    import numpy as np
    
    bs = ms.BubbleScaler()
    bubble_df = bs.scale_map(df, 'scaleby', usa_albers=True, 
                   map_vel=.001, group_vel=.15, verbose=True)

If ``verbose``, :func:`~mapscaler.BubbleScaler.scale_map` will print progress as it goes (truncated below):

.. code-block:: none

    Iteration 1
    --93 overlapping groups remaining
    Iteration 2
    --89 overlapping groups remaining
    ...
    [truncated]
    ...
    Iteration 42
    --2 overlapping groups remaining
    Iteration 43
    --2 overlapping groups remaining
    Iteration 44
    Separated in 44 iterations 

Now, let's visualize the output ``bubble_df``:
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
        bubble_df, hue=[np.log(x) for x in df.EST_POP_2019],
        figsize=(15,8), linewidth=0, cmap='viridis',
    )
    plt.title('AFTER', fontsize=30, loc='left')
    plt.show()


Documentation
^^^^^^^^^^^^^^

.. currentmodule:: mapscaler
.. autoclass:: BubbleScaler
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
