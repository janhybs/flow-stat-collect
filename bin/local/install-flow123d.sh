#!/bin/bash

# path where flow123d repository is
FLOW_LOC=$1

## use clang
#export CC=/usr/bin/clang
#export CXX=/usr/bin/clang++

# build flow
cd $FLOW_LOC
git -C bin/docker checkout -f master
make -j4 all

ldd bin/flow123d

# update python to latest
F=$FLOW_LOC
D=/home/jan-hybs/Dokumenty/projects/Flow123dDocker/flow123d
set -x

rm -rf $F/lib/python/flow123d
rm -rf $F/src/python
rm -rf $F/bin/python

cp -rf $D/src/python $F/lib/python/flow123d
cp -rf $D/src/python $F/src/python
cp -rf $D/bin/python $F/bin/python

#
## create python libs
#mkdir -p $FLOW_LOC/lib/python
#cd $FLOW_LOC/lib/python
#
##rm -rf dist-packages
##pip install --target dist-packages \
##    pyyaml \
##    markdown \
##    psutil \
##    simplejson \
##    formic==0.9beta \
##    pymongo
#
#ls -ls dist-packages
