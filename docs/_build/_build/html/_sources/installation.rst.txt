============
Installation
============

.. toctree::
   :maxdepth: 2

Third Parties Requirements
---------------------------

 - Schrodinger > 2016

 - Pele > 1.5


Conda(Recommended)
---------------------------------

::

  conda create --name msm_pele python=3.6

  source activate msm_pele

  conda install -c NostrumBioDiscovery msm_pele

  change schrodinger & PELE constants path on your machine under site-packages/msm_pele/constants.py


Pypi
-------------------

::

  pip install msm_pele
  
  change schrodinger & PELE constants path on your machine under site-packages/msm_pele/constants.py


Source Code 
---------------------------

::

  git clone https://github.com/NostrumBioDiscovery/msm_pele.git

  python MSM_PELE/setup.py install

  change schrodinger & PELE constants path on your machine under site-packages/msm_pele/constants.py


Update latest changes from Github Code (once already installed)
-------------------------------------------------------------------

::

 cd MSM_FOLDER
 cp constants.py ../save_loc/
 git stash
 git pull origin master
 cp ../save_loc/constants.py .

If you do not want to copy the constants.py every time you can 
add your machine paths there and pull request to the repository.


