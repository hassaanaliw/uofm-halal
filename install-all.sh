#!/usr/bin/env bash

######### Install Python virtual environment ########
source env/bin/activate

######## Node and Node Virtualenv Installation #########
./env/bin/pip install nodeenv
nodeenv --python-virtualenv
source ./env/bin/activate

# Install Javascript packages
npm install .

# Build React Code
./node_modules/.bin/webpack


