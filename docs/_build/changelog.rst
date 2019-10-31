============
Changelog
============

.. toctree::
   :maxdepth: 2


Here we report all MSM changes thorugh all different releases on: `MSM github <https://github.com/danielSoler93/MSM_PELE/releases>`_

2.1 - 28-10-2019
---------------------------------
    - Add water MC step
    - Deprecate receptor.pdb + .mae input
    - Paper released
    - Fix minor bugs


2.0 - 21-02-2019
---------------------------------

    - Improved installation (conda still not supported due to commercial dependencies)
    - Add the possibility of performing several iterations in one job
    - Add the possibility of performing a MSM estimation after each run
    - Add a new MultipleBox module to limit exploration
    - Improved control file
    - Fixing minor bugs

1.1.0 - 02-10-2018
-----------------------
    - Kill simulation by time and assess MSM and convergence
    - Minor improvements on implementation
    - Build better documentation

1.0.3 - 4-07-2018
-----------------------

    - .xtc output implemented
    - Make control file automatically for each system
    - Other Minor Changes

1.0.2 - 4-05-2018
--------------------
    - Add the possibility of running MSM with two different levels of exhaustiveness
    - Add rotamer resolution option 
    - Add the possibility of specifying output folder name
    - Include first version of tICA

1.0.1 - 3-16-2018
-------------------
    - First automatic pipeline: pele exit + pele exploration + MSM analysis
