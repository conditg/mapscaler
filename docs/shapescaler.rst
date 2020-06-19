.. _ss:

Shape Scaler
=================

Simple Example
^^^^^^^^^^^^^^^^

NOTE: This example uses the variable ``df`` as seen in the example in :ref:`lcm`.
::

    import mapscaler as ms
    ss = ms.ShapeScaler()
    new_df = ss.scale_map(df, 'scaleby', verbose=True)

If ``verbose``, Shape Scaler will print progress as it goes (truncated below):

.. code-block:: none

    Iteration 1
    --79 overlapping groups remaining
    ...
    [truncated]
    ...
    Iteration
    -- overlapping groups remaining
    Separated in 

Now, let's visualize the output:




Documentation
^^^^^^^^^^^^^^
.. currentmodule:: mapscaler
.. autoclass:: ShapeScaler
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
