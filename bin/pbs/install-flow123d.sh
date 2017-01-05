#!/bin/bash
#PBS -N install-flow
#PBS -l mem=4gb
#PBS -l scratch=1gb
#PBS -l nodes=1:ppn=3
#PBS -l walltime=01:30:00
#PBS -j oe
# ::  qsub -l walltime=1h -l nodes=1:ppn=3,mem=4gb -I
# ::  qsub -l walltime=1:00:00 -l select=1:ncpus=2:mem=4gb -I

# path where flow123d repository is
FLOW_LOC=$1


exit 1
# need to load following modules in order to build flow123d and its libs
module purge
module load /software/modules/current/metabase
module load cmake-2.8.12
module load gcc-4.9.2
module load boost-1.56-gcc
module load perl-5.20.1-gcc
module load openmpi

module load python27-modules-gcc
module load python-2.7.10-gcc

module unload gcc-4.8.1
module unload openmpi-1.8.2-gcc

# make flow
cd $FLOW_LOC
make -j4 all

ldd bin/flow123d

create python libs
mkdir -p $FLOW_LOC/lib/python
cd $FLOW_LOC/lib/python

rm -rf dist-packages
pip install --target dist-packages \
    pyyaml \
    markdown \
    psutil \
    simplejson \
    formic \
    pymongo

ls -ls dist-packages
