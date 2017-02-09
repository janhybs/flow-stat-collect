#!/bin/bash

# get script location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get script location
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"


# load module for pip3
module load python34-modules-gcc

# install all requirements
pip3 install -r $PROJECT_ROOT/libs/requirements.txt --target $PROJECT_ROOT/libs