**********
User Guide
**********

To use pyiat, data from the Implicit Association Test (IAT) or Brief IAT (BIAT) must contain all trials for all subjects in a pandas DataFrame. If the IAT/BIAT paradigm software produces single files for each participant, then you must concatanate all these data together into a single file and import into pandas prior to using pyiat. 

Installing pyiat
=============================================

::

    pip install pyiat

Importing pyiat
==========================================

::

    import pyiat

Using pyiat
==========================================

    To run the standard weighted IAT scoring algorithm that will return a dataframe error percentages, percentages of too fast/too slow trials, poor performance flags (e.g. a subject made more errors than the cutoff for poor performance) and D scores, enter 
    -the pandas dataframe, 
    -column containing subject numbers, 
    -column containing reaction time, 
    -column containing the condition for each trial, 
    -column containing accuracy where 1 is correct and 0 is an error (can enter an argument to switch where error is 1 and correct is 0) 
    -the name of each condition (maximum 2), 
    -the column containing block number and 
    -a list of which 4 blocks 

::

    d1=analyze_iat(d,subject='subjnum',rt='latency',condition='condition',correct='correct',cond1='Death/Not Me,Life/Me',cond2='Life/Not Me,Death/Me',block='block',blocks=[2,3,5,6])


    To run an unweighted IAT scoring algorithm just add the argument 'weighted = True'. The unweighted algorithm will not provide output by block. 

::

    d1=analyze_iat(d,subject='subjnum',rt='latency',condition='condition',correct='correct',cond1='Death/Not Me,Life/Me',cond2='Life/Not Me,Death/Me', weighted=True)

More examples

    For more details of the input, output and more examples of pyiat see the `Jupyter notebook`_ located on Github. There is also simulated data on Github_ as well. 


.. _`Jupyter notebook`: https://nbviewer.jupyter.org/github/amillner/pyiat/blob/master/example/pyiat_example.ipynb
.. _Github: https://github.com/amillner/pyiat/tree/master/example
