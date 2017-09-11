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

- the pandas dataframe contain raw IAT data
- column containing subject numbers
- column containing reaction time
- column containing the condition for each trial
- column containing accuracy where 1 is correct and 0 is an error (can enter an argument to switch where error is 1 and correct is 0) 
- the name of each condition (maximum 2)
- the column containing block number and
- a list of which 4 blocks

::

    d1=pyiat.analyze_iat(d,subject='subjnum',rt='latency',condition='condition',correct='correct',cond1='Death/Not Me,Life/Me',cond2='Life/Not Me,Death/Me',block='block',blocks=[2,3,5,6])


To run an unweighted IAT scoring algorithm just add the argument 'weighted = True'. The unweighted algorithm will not provide output by block. 

::

    d1=pyiat.analyze_iat(d,subject='subjnum',rt='latency',condition='condition',correct='correct',cond1='Death/Not Me,Life/Me',cond2='Life/Not Me,Death/Me', weighted=True)

Additional features
==========================================

- Setting reaction times considered too fast or too slow, set arguments 'fast_rt' and/or 'slow_rt', default : 400, 10000
- Can set flags for poor performance and exclusion criteria for errors, or fast and slow trials and can set by overall rates, rates by block or rates by condition.
- Can flag anyone who has less than a specific number of blocks, default : 4 (only applies to weighted algorothm)
- Can output a second dataframe containing the overall number and percentage of trials removed because they were too fast or too slow. Returns this information across all subjects as well as across just thost without flags for poor performance.
- Can analyze the Brief IAT by setting 'biat' argument to *True*. When analyzing the biat, you can set the number of trials to remove from the beginning of each block ('biat_rmv_xtrls', default : 4) but you have to give pyiat the column that contains the trial number for each trial in the argument 'biat_trl_num'.
- Can return D score for each stimulus (word) in the IAT. This score can be weighted or unweighted, although weighted will return fewer scores because some blocks may not contain a word. This can be used with BIAT as well, although it is recommended you use unweighted as weighted results in many similar D scores because there is a word is often present only once a block.  

-See the :doc:'Arguments documentation <arguments>'

Additional options
==========================================

-Can enter an accuracy column where correct is 1 and errors are 0 (default) or where errors are 1 and correct or 0 by entering *error* for the argument 'error_or_correct'.
-Currently, pyiat reports percentage of errors prior to removing all trials where reaction time was too fast or too slow. Setting the argument 'errors_after_fastslow_rmvd' to *True* will calculate error rate after removing all too fast or too slow trials. This is the way the R package iat calculates error rate. 
-To return the nuumber of errors and too fast\too slow trials rather than percentages set the 'flag_outformat' to *count*.
-Output an Excel files with all returned data by setting 'print_to_excel' to *True*.

-See the :doc:'Arguments documentation <arguments>'

Examples
------------------------------------------------
    For more details of the input, output and more examples of pyiat see the `Jupyter notebook`_ located on Github. There is also simulated data on Github_ as well. 


.. _`Jupyter notebook`: https://nbviewer.jupyter.org/github/amillner/pyiat/blob/master/example/pyiat_example.ipynb
.. _Github: https://github.com/amillner/pyiat/tree/master/example
