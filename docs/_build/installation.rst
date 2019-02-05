============
Installation
============

.. toctree::
   :maxdepth: 2

MSM PELE installation requires several dependencies they must be set
before practice. Furthermore MSM PELE requires Schrodinger and PELE installation.

Conda Installation (Recommended)
---------------------------------

**Create conda**::

  conda create --name py36 python=3.6

**Activate Env**::

  source activate py36

**Install software**::

  from the folder containing MSM_PELE and with the python used to run the software later:

  python MSM_PELE/setup.py install --schr </path/to/schrodinger> --pele </path/to/pele/> --pele-license </path/to/pele/licenses> --pele-exec </path/to/pele/bin> --mpirun </path/to/mpi> 

MSM PELE Configuration
-----------------------

**Enviromental variables**::
 
  export PYTHONPATH=$PYTHONPATH:'/path/to/MSM_PELE/'


**Pyemma config**::

  $ python

  > import pyemma

  > pyemma.config.used_filenames

You will recieve a list with files where it is possible to find configuration from pyemma. You need to go over these files and change::

    show_progress_bars = Flase

    mute= True
