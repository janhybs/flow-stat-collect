#!/bin/bash

# get script location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get script location
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"


# run frontend script
python3 $PROJECT_ROOT/src/time-machine.py "$@"
