.. _lcm:

Loading Common Maps
======================

Simple Example 
^^^^^^^^^^^^^^^^

Import MapScaler and load a map of the US Counties:
::

    import mapscaler as ms
    loader = ms.MapLoader()
    df = loader.fetch_counties()['df']

That's it! You now have a map of the counties. 
::

    import matplotlib.pyplot as plt
    import geoplot as gplt

    #Reduce to the lower 48 for an easier demonstration
    df = df[df.STATE_FIPS != '02'] # remove AK
    df = df[df.STATE_FIPS != '15'] # remove HI
    df = df[df.STATE_FIPS != '72'] # remove PR
    
    gplt.polyplot(
        df, 
        projection=gplt.crs.AlbersEqualArea(),
        figsize=(15,8),
        )
    plt.suptitle('Contiguous United States', fontsize=20, ha='center')
    plt.show()

.. image:: ../images/counties.png
   :alt: US Counties
   :align: center



Documentation
^^^^^^^^^^^^^^

.. currentmodule:: mapscaler
.. autoclass:: MapLoader
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
