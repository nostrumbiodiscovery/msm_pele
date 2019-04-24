============
Installation
============

.. toctree::
   :maxdepth: 2

MSM PELE installation requires several dependencies they must be set
before practice. Furthermore MSM PELE requires Schrodinger and PELE installation.

Conda Installation (Recommended)
---------------------------------

**Instructions**::

  conda create --name py36 python=3.6

  source activate py36

  git clone https://github.com/danielSoler93/MSM_PELE.git

  pip install numpy cython

  python MSM_PELE/setup.py install --schr </path/to/schrodinger> --pele </path/to/pele/> --pele-license </path/to/pele/licenses> --pele-exec </path/to/pele/bin> --mpirun </path/to/mpi> 

  export $PYTHONPATH=$PYTHONPATH:/folder/before/MSM_PELE/:/folder/MSM_PELE/


Source Code Installation
---------------------------

**Instructions**::
    
  git clone https://github.com/danielSoler93/MSM_PELE.git

  python MSM_PELE/setup.py install --schr </path/to/schrodinger> --pele </path/to/pele/> --pele-license </path/to/pele/licenses> --pele-exec </path/to/pele/bin> --mpirun </path/to/mpi> 

  export $PYTHONPATH=$PYTHONPATH:/folder/before/MSM_PELE/:/folder/MSM_PELE/

Update latest changes from Github Code (once already installed)
-------------------------------------------------------------------

**Instructions**::
 
 cd MSM_FOLDER
 cp constants.py ../save_loc/
 git stash
 git pull
 cp ../save_loc/constants.py .

 If you do not want to copy the constants.py every time you can 
 add your machine paths there and pull request to the repository.


