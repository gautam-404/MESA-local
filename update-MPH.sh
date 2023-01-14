#! /usr/bin/env zsh

###### MesaProjHandler ######

if [[ "$OSTYPE" == "linux"* ]]; then
    cd $HOME/software     ## For my gitpod
elif [[ "$OSTYPE" == "darwin"* ]]; then
    cd /Users/anuj/Documents/MESA-workspace     ## for my mac
fi

rm -rf MesaProjHandler
git clone --recurse-submodules https://github.com/gautam-404/MesaProjHandler.git
cd MesaProjHandler
pip3 install .