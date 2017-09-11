pyiat |release|
=================

pyiat analyzes data from the Implicit Association Test (IAT) consistent with the standard IAT scoring algorithm (Greenwald et al., 2003) and Brief IAT scoring algorithm (Nosek et al., 2014)

Greenwald, A. G., Nosek, B. A., & Banaji, M. R. (2003). Understanding and using the Implicit Association Test: I. An improved scoring algorithm. Journal of Personality and Social Psychology, 85(2), 197–216. https://doi.org/10.1037/0022-3514.85.2.197

Nosek, B. A., Bar-Anan, Y., Sriram, N., Axt, J., & Greenwald, A. G. (2014). Understanding and Using the Brief Implicit Association Test: Recommended Scoring Procedures. PLOS ONE, 9(12), e110938. https://doi.org/10.1371/journal.pone.0110938


Use the :doc:`Quickstart<quickstart>` guide for installation instructions and usage.

Features
--------

pyiat currently supports:

* Analysis of the IAT and Brief IAT (BIAT) 
* IAT can be analyzed with weighted or unweighted algorithm
* BIAT can include 1, 2, or 3 blocks 
* Can obtain D scores for each stimulus (word)
* Output includes overall error percentage as well as error percentages by block (if using a weighted score) and by condition 
* Same output (overall, by block, by condition) for trials considered too fast or too slow
* Can set reaction time for trials considered too fast or too slow
* Can set cutoffs for error\too fast\too slow flags indiciating that a participant is excluded for poor performance
* Can print output to Excel

Source code
-----------

You can access the source code at: https://github.com/amillner/pyiat

How to get help, contribute, or provide feedback
------------------------------------------------

See our :doc:`feedback and contribution submission guidelines <contribute>`.

Documentation
-------------

.. toctree::
   :maxdepth: 2

   install
   userguide
   arguments