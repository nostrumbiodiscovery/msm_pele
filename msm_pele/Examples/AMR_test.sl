#!/bin/bash
#SBATCH -J PELE_MPI
#SBATCH --output=mpi_%j.out
#SBATCH --error=mpi_%j.err
#SBATCH --ntasks=10
#SBATCH --qos=debug

module purge
unset PYTHONPATH
unset LD_LIBRARY_PATH
module purge
module load icc/2018.1.163-GCC-6.4.0-2.28 intel imkl  impi Python/2.7.14-intel-2018a  intel imkl  impi Python Boost/1.66.0-intel-2018a  CMake/3.9.5-GCCcore-6.4.0 patchelf/0.9-intel-2018a wjelement/1.3-intel-2018a JsonCpp/1.8.4-intel-2018a GCC/6.4.0-2.28
module load impi/2018.1.163-iccifort-2018.1.163-GCC-6.4.0-2.28 Boost/1.66.0-intel-2018a wjelement/1.3-intel-2018a
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
export PYTHONPATH=/work/NBD_Utilities/PELE/PELE_Softwares/msm_pele/:/work/NBD_Utilities/PELE/PELE_Softwares/adaptive_types/v1.6.2/:$PYTHONPATH

python -m msm_pele.main URO_INIT.pdb AMR L --mae_lig 1F5L.mae --test  --iterations 3
