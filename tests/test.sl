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
export PYTHONPATH=/gpfs/projects/bsc72/MSM_XTC/bin/v2.0.0/:/gpfs/projects/bsc72/MSM_XTC/bin/v2.0.0/MSM_PELE/:/gpfs/projects/bsc72/lib/site-packages/:/gpfs/projects/bsc72/lib_msm/site-packages/:$PYTHONPATH
#Run tests
pytest /gpfs/projects/bsc72/MSM_XTC/bin/v2.0.0/MSM_PELE/test/ -vv > out.txt
