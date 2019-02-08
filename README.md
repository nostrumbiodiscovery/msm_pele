# MSM_Pele
--------------
Monte Carlo Protein Energy Landscape Exploration (PELE) coupled with Markov State Model (MSM) analysis  with the aim to calculate absolute free energies.

# MSM_Pele's PipeLine
-------------------------------
1) [Protein Preparation for Pele](https://github.com/Jelisa/mut-prep4pele)
2) [PlopRotTemp_SCHR2017](https://github.com/miniaoshi/PlopRotTemp_S_2017)
3) [Adaptive PELE](https://github.com/AdaptivePELE/AdaptivePELE)
4) [PELE(comercial software)](https://pele.bsc.es/pele.wt)
5) [MSM](https://github.com/miniaoshi/Pele_scripts)

# Installation
-------------------
0) git clone https://github.com/miniaoshi/MSM_PELE.git

1) python MSM_PELE/setup.py install --schr </path/to/schrodinger> --pele </path/to/pele/> --pele-license </path/to/pele/licenses> --pele-exec </path/to/pele/bin> --mpirun </path/to/mpi>

i.e python MSM_PELE/setup.py install --scht /opt/schrodinger-2017/ --pele /opts/pelerev1234 --pele-license /opts/pelerev1234/license --pele-exec /opts/pelerev1234/bin/ --mpirun /usr/bin/mpirun


# Documentatin:
---------------

- https://danielsoler93.github.io/MSM_PELE/
