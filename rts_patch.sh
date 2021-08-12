#!/bin/bash -l
#SBATCH --job-name=rts_1194628776
#SBATCH --output=RTS-patch-1194628776-%A.out
#SBATCH --nodes=25
#SBATCH --time=01:00:00
#SBATCH --clusters=garrawarla
#SBATCH --partition=gpuq
#SBATCH --account=mwaeor
#SBATCH --export=NONE
#SBATCH --gres=gpu:1

module use /pawsey/mwa/software/python3/modulefiles
module load RTS/sla_to_pal
module load python-singularity

set -eux
command -v rts_gpu
export UCX_MEMTYPE_CACHE=n

date
srun -n 25 --export=ALL rts_gpu rts_patch.in
date
# Allow python scripts to fail.
set +e
srun -n 1 -N 1 --export=ALL plot_BPcal_128T.py --both --outname BPcal.png
srun -n 1 -N 1 --export=ALL plot_CalSols.py
set -e
date

#date
#time srun -n 25 --export=ALL rts_gpu rts_peel.in
#date

# Ensure permissions are sensible!
find . -user "${USER}" -type d -exec chmod g+rwx,o+rx,o-w {} \;
find . -user "${USER}" -type f -exec chmod g+rw,o+r,o-w {} \;
