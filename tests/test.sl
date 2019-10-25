#!/bin/bash
#SBATCH -J PELE_MPI
#SBATCH --output=mpi_%j.out
#SBATCH --error=mpi_%j.err
#SBATCH --ntasks=4 #Minimum number of cpus

#Export need it modules for Python & PELE
module purge
module load  
unset PYTHONPATH
#Charge MSM and MSM/AdaptivePELE inside the path if they are not in the default python libraries
export PYTHONPATH=/path/to/folder/before_msm_pele/:/path/to/folder/msm_pele/:/gpfs/projects/bsc72/lib/site-packages/:/gpfs/projects/bsc72/lib_msm/site-packages/:$PYTHONPATH
#Run tests
pytest . -vv > out.txt
