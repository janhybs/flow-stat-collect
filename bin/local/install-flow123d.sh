#!/bin/bash

# path where flow123d repository is
FLOW_LOC=$1

## use clang
#export CC=/usr/bin/clang
#export CXX=/usr/bin/clang++

# make flow
cd $FLOW_LOC
make -j4 all

ldd bin/flow123d

# create python libs
mkdir -p $FLOW_LOC/lib/python
cd $FLOW_LOC/lib/python

rm -rf dist-packages
pip install --target dist-packages \
    pyyaml \
    markdown \
    psutil \
    simplejson \
    formic==0.9beta \
    pymongo

ls -ls dist-packages
