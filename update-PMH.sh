#! /usr/bin/env zsh

if [[ "$OSTYPE" == "linux"* ]]; then
    cd $HOME/software     ## For my gitpod
elif [[ "$OSTYPE" == "darwin"* ]]; then
    cd /Users/anuj/Documents/MESA-workspace     ## for my mac
fi

rm -rf PyMesaHandler
git clone --recurse-submodules https://github.com/gautam-404/PyMesaHandler.git
cd PyMesaHandler
pip3 install -r requirements.txt
pip3 install .