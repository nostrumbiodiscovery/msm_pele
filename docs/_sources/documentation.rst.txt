==============
Documentation
==============

.. toctree::
   :maxdepth: 2


Pipeline Arguments
-------------------



  - **Protein Preparation for Pele**:

    The input complex will be processed by the software checking  next features:

    - HIS/HIP/HID will be transform into PELE language.

    - Capping loops will be neutral

    - Constraints will be applied every 10 Calphas on the receptor complex.

    - Constraints will be applied on all metals and its coordinates.

    - Partial missing sidechains will be added

    - Template residues and non standard aminoacids will be checked

    - Other found errors will be outputted to screen for the user to change them manually. 

    |    

  - **Adaptive Exit**:

    An adaptive PELE exit simulation will be performed over the docked complex until 5 trajectories reach a SASA bigger than 0.95. Then, the exit path will be clusterize using KMeans algorithm and this will serve as input on the next PELE explortion simulation.
  
  .. figure:: adaptive_out.png
    :scale: 80%
    :align: center
    :alt: Install need it plugin to visualize the Adaptive exit simulation

    Clusters of two Adaptive exit simulations with different ligands over the
    same target    

  - **Pele Exploration**:
  
  A PELE exploration will be performed with all the previous cluster as
  different initial postions of the ligand to explore as much transitions as
  posible between the slowest binding modes. Then, points will be clusterize
  through a KMeans algorithm.


  .. figure:: pele.png
    :scale: 80%
    :align: center
    :alt: Install need it plugin to visualize PELE simulation

    PELE MC simulation clusters
   

  - **MSM Analysis**:
  
  Finally, the transition matrix will be computed and diagonilize for several
  subsets of the previous data. Using thermodinamic stadistic on the subset's
  eigenvectors, absolute free energies and its standard deviation can be
  stimated as well as system's markovianity.



Restart
--------


  - **- - restart** restart the simulation from [adaptive, pele, msm]:

    + **adaptive**  flag will luch the exit simulation with the already processed input pdb. 
    + **pele** flag will lunch a Monte Carlo simulation that will be later analyse via MSM.
    + **msm** flag will  perform MSM analysis over the previous monte carlo simulation.
    + **analyse** flag will perform the analysis of the MSM extracting representative structures
        and PMF and probability plots.
  
i.e.0 python -m MSM_PELE.main complex.pbd resname chain --restart [adaptive, pele, msm, analyse]

i.e.1 python -m MSM_PELE.main complex.pbd LIG Z --restart adaptive

i.e.2 python -m MSM_PELE.main complex.pbd LIG Z --restart pele

i.e.3 python -m MSM_PELE.main complex.pbd LIG Z --restart msm


Input Preparation
-----------------

- **--charge_ter** to charge all terminal resiues of the receptor.
 i.e.0 python -m MSM_PELE.main complex.pbd resname chain --charge_ter
 i.e.1 python -m MSM_PELE.main complex.pbd LIG Z --charge_ter

- **--gaps_ter** cap gaps or leave them as connected atoms.
  i.e.0 python -m MSM_PELE.main complex.pbd resname chain --gaps_ter
  i.e.1 python -m MSM_PELE.main complex.pbd LIG Z --gaps_ter

- **--forcefield** forcefield to use to describe the protein. Options:
  i.e. python -m MSM_PELE.main complex.pbd resname chain --forcefield [OPLS2005 (default), Amber99sb]
  i.e.1 python -m MSM_PELE.main complex.pbd LIG Z --forcefield OPLS2005

- **--core** Specify an atom from the ligand that will be use as center of a 
  rigid core to identify flexible sidechains and rotamers
  i.e.0 python -m MSM_PELE.main complex.pbd resname chain --core atomnumber
  i.e.1 python -m MSM_PELE.main complex.pbd LIG Z --core 1456

- **--mtor** Maximum number of rotamers per sidechain [defaut=4]
  i.e.0 python -m MSM_PELE.main complex.pbd resname chain --mtor number
  i.e.1 python -m MSM_PELE.main complex.pbd LIG Z --mtor 3

- **--n** Maximum number of sidechains [default=None]
  i.e.0 python -m MSM_PELE.main complex.pbd resname chain --n number
  i.e.1 python -m MSM_PELE.main complex.pbd LIG Z --n 10

- **--gridres** Rotamers resolution. Every how many degrees the rotamers will
  be moved in simulation. As bigger the faste the sofware while loosing exploration.
  [default=10]
  i.e. python -m MSM_PELE.main complex.pbd resname chain --gridres (degrees of rotation)
  i.e. python -m MSM_PELE.main complex.pbd LIG Z --gridres 30

Adaptive Exit simulation
-------------------------

- **--clust** number of clusters after adaptive exit simulation. It must always
  be smaller than the number of cpu power. [default=40]
  i.e.0 python -m MSM_PELE.main complex.pbd resname chain --clust number_of_clusters
  i.e.1 python -m MSM_PELE.main complex.pbd LIG Z --clust 60

- **--cpus** number of cpus to use [default=50]
  i.e.0 python -m MSM_PELE.main complex.pbd resname chain --cpus number_of_cpus
  i.e.1 python -m MSM_PELE.main complex.pbd LIG Z--cpus 128

Exploration
-----------

- **--confile** Use your own pele exploration configuration file
  i.e.0 python -m MSM_PELE.main complex.pbd resname chain --confile
  /path/to/myconfile.conf
  i.e.1 python -m MSM_PELE.main complex.pbd LIG Z --confile pele.conf

- **precision** Use a more aggresive control file. Useful when dealing
  with higly charged and exposed ligands. 
  i.e.0 python -m MSM_PELE.main complex.pbd resname chain --precision

- **test** Run short test after. Usefull after instalation.
  i.e.0 python -m MSM_PELE.main complex.pbd resname chain --test
  i.e.1 python -m MSM_PELE.main complex.pbd LIG Z --test

- **user_center** Define the center of the exploration box. Must be use together with 
   user_radius.

- **user_radius** Define the radiues of the box
  i.e.0 python -m MSM_PELE.main complex.pbd resname chain --user_center center_coords (A) --user_radius radius (A)
  i.e.0 python -m MSM_PELE.main complex.pbd LIG Z --user_center 22.5 -46.67 2.1 --user_radius 20

