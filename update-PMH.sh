#! /usr/bin/env zsh

cd $HOME/software     ## For my gitpod
# cd /Users/anuj/Documents/MESA-workspace     ## for my mac
rm -rf PyMesaHandler
git clone --recurse-submodules https://github.com/gautam-404/PyMesaHandler.git
cd PyMesaHandler
pip3 install -r requirements.txt
pip3 install .