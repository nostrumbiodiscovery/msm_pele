==================
Parameters
==================

.. toctree::
   :maxdepth: 2

Required Paramaters:
------------------------

OPLS2005 charges
++++++++++++++++++

If you want to use OPLS2005 charges:

- **complex.pdb** initial pdb with receptor and ligand already docked

- **resname** residue name of the ligand

- **chain** chain of the ligand

- **--cpus** number of cpus to use

- **--time** number of seconds to run each iteration

- **--temp** temperature to run the simulation (binding exposed cavities 1500, charged ligands 1500, other 1000)

::

    i.e.0 python -m msm_pele.main complex.pbd resname chain --cpus number_cpus --time seconds --temp temperature
    
    i.e.1 python -m msm_pele.main complex.pbd LIG Z  --cpus 128 --time 25000 --temp 1000

QM charges
+++++++++++

If you want to use external charges:

- **receptor.pdb** pdb of the receptor with the bound conformation to the docked ligand

- **resname** residue name of the ligand

- **chain** chain of the ligand

- **--mae_lig ligand.mae** mae file of the ligand with QM charges 

- **--cpus** number of cpus to use

- **--time** number of seconds to run each iteration

- **--temp** temperature to run the simulation (binding exposed cavities 1500, charged ligands 1500, other 1000)


::

    i.e.0 python -m msm_pele.main complex.pbd resname chain --mae_lig ligand.mae --cpus number_cpus --time seconds --temp temperature
    
    i.e.1 python -m msm_pele.main complex.pbd LIG Z --mae_lig ligand.mae --cpus 128 --time 25000 --temp 1000

Output Parameters
-------------------


- **--folder** specify the output name of the folder

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --folder folder_name

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --folder LIG_MSM

- **--pdb** use pdb format as output file (default=.xtc)

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --pdb

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --pdb

- **--log** print a log simulation file for each CPU whenever running a PELE simulation

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --log

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --log


Restart Parameters
-------------------


  - **- - restart** restart the simulation from [adaptive, pele, msm]:

    + **adaptive**  flag will luch the exit simulation with the already processed input pdb. 
    + **pele** flag will lunch a Monte Carlo simulation that will be later analyse via MSM.
    + **msm** flag will  perform MSM analysis over the previous monte carlo simulation.
    + **analyse** flag will perform the analysis of the MSM extracting representative structures
        and PMF and probability plots.

::

    i.e.0 python -m msm_pele.main complex.pbd resname chain --restart [adaptive, pele, msm, analyse]

    i.e.1 python -m msm_pele.main complex.pbd LIG Z --restart adaptive

    i.e.2 python -m msm_pele.main complex.pbd LIG Z --restart pele

    i.e.3 python -m msm_pele.main complex.pbd LIG Z --restart msm


Input Preparation Parameters
-----------------------------

receptor
++++++++++++++

The input complex will be processed by the software checking  next features:

- **--charge_ter** to charge all terminal resiues of the receptor.

::

 i.e.0 python -m msm_pele.main complex.pbd resname chain --charge_ter

 i.e.1 python -m msm_pele.main complex.pbd LIG Z --charge_ter

- **--gaps_ter** cap gaps or leave them as connected atoms.

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --gaps_ter

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --gaps_ter

- **--forcefield** forcefield to use to describe the protein. Options:

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --forcefield [OPLS2005 (default), Amber99sb]

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --forcefield OPLS2005

ligand
++++++++++

- **--core** Specify an atom from the ligand that will be use as center of a 
  rigid core to identify flexible sidechains and rotamers

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --core atomnumber

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --core 1456

- **--mtor** Maximum number of rotamers per sidechain [defaut=4]

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --mtor number

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --mtor 3

- **--n** Maximum number of sidechains [default=None]

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --n number

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --n 10

- **--gridres** Rotamers resolution. Every how many degrees the rotamers will
  be moved in simulation. As bigger the faste the sofware while loosing exploration.
  [default=10]

::

  i.e. python -m msm_pele.main complex.pbd resname chain --gridres (degrees of rotation)

  i.e. python -m msm_pele.main complex.pbd LIG Z --gridres 30

Exit Simulation Parameters
----------------------------

- **--clust** number of clusters after adaptive exit simulation. It must always
  be smaller than the number of cpu power. [default=40]

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --clust number_of_clusters

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --clust 60

- **--cpus** number of cpus to use [default=50]

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --cpus number_of_cpus

  i.e.1 python -m msm_pele.main complex.pbd LIG Z--cpus 128

Exit simulation clustering Parameters
-------------------------------------

An adaptive PELE exit simulation will be performed over the docked complex until 5 trajectories reach a SASA bigger than 0.95. Then, the exit path will be clusterize using KMeans algorithm and this will serve as input on the next PELE explortion simulation.

- **--no_sasa** Cluster with K-means and start from all clusters with the same probability 

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --no_sasa

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --no_sasa

- **--sasa** Cluster with K-means and divide clusters in 3 intervals
  of treshold: [x<sasa_min, sasa_min<x<sasa_max, x>sasa_max]. 25% of the processors
  will start from clusters of the first interval, 50% from the second one and another
  25% from the third.

::

  i.e.0 python -m msm_pele.main complex.pbd complex.pbd resname chain --sasa (minimum sasa value, maximum sasa value)

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --sasa 0.2 0.6 (25% of the processors will starts from
  clusters of the exit simulation under sasa 0.2, 50% on clusters with sasa in between 0.2 and 0.6  and
  25% on the clusters with more than sasa 0.6).

- **--perc_sasa** Cluster with K-mean and divide the three intervals explained above 
  between the processors with probability [x,y,z] default [0.25, 0.5, 0.25]

::

  i.e.0 python -m msm_pele.main complex.pbd complex.pbd resname chain --perc_sasa (percentage1, percentage2, percentage3)  

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --perc_sasa 0.3 0.6 0.1

Box Parameters
---------------

- **--box_type** One single big box to most conformational space or multiple 
  little boxes to limit this and speed up calculations. default [multiple]

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --box_type (type of box)

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --box_type fixed

  i.e.2 python -m msm_pele.main complex.pbd LIG Z --box_type multiple

- **--box** Use box from other simulations. default [None]

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --box (pdb with box)

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --box box.pdb

- **--user_center** Specfy a single or multiple centers of the box . default [None]
  **--user_radius** Specfy a single or multiple radius of the box . default [None]

  user_center & user_radius  must be used together.

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --user_center (centerx centery centerz) --user_radius (radius)

  i.e.0 python -m msm_pele.main complex.pbd resname chain --user_center 22.2 -3.4 12.5 --radius 22 (1 box)

  i.e.0 python -m msm_pele.main complex.pbd resname chain --user_center 22.2 -3.4 12.5 31.24 32.59.76 --radius 21 8 (2 boxes)

Exploration Parameters
-------------------------
  
A PELE exploration will be performed with all the previous cluster as
different initial postions of the ligand to explore as much transitions as
posible between the slowest binding modes. Then, points will be clusterize
through a KMeans algorithm.

metrics
++++++++++

- **--native** calculate RMSd of each step in respect to an external pdb

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --confile
  /path/to/myconfile.conf --native native.pdb

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --confile pele.conf 
  --native x_ray_complex.pdb

waters
+++++++

- **--water** waters to move using MC water exploration step.
  All other waters will be automatically constrained.

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --water chain_water:residue_water

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --water M:1 M:2

- **--water_radius** radius of the exploration box in the water's MC

::

  i.ei.0 python -m msm_pele.main complex.pbd resname chain --water M:1 --water_radius radius_of_box (Angstroms)

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --water M:1 M:2 --water_radius 7

- **--water_temp** temperature parameter in the water's MC

::

  i.ei.0 python -m msm_pele.main complex.pbd resname chain --water M:1 --water_temp temperature (K)

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --water M:1 M:2 --water_temp 1000

- **--water_trials** steric trials parameter in the water's MC

::

  i.ei.0 python -m msm_pele.main complex.pbd resname chain --water M:1 --water_trials number_of_trials

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --water M:1 M:2 --water_trials 2000

- **--water_constr** constrain applied to the waters during the minimization that follows the water perturbation. Slightly forces the water to keep in place to avoid them to shift because of steric clashes of the sidechains.

::

  i.ei.0 python -m msm_pele.main complex.pbd resname chain --water M:1 --water_constr constraint (kcal/mol)

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --water M:1 M:2 --water_constr 3.

protocol
++++++++++++++

- **--confile** Use your own pele exploration configuration file

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --confile
  /path/to/myconfile.conf

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --confile pele.conf

- **precision** Use a more aggresive control file. Useful when dealing
  with higly charged and exposed ligands. 

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --precision


- **test** Run short test after. Usefull after instalation.

::

  i.e.0 python -m msm_pele.main complex.pbd resname chain --test

  i.e.1 python -m msm_pele.main complex.pbd LIG Z --test


MSM Analysis
--------------

Finally, the transition matrix will be computed and diagonilize for several
subsets of the previous data. Using thermodinamic stadistic on the subset's
eigenvectors, absolute free energies and its standard deviation can be
stimated as well as system's markovianity.
