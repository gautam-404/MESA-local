#! /usr/bin/zsh

cd $HOME/software
rm -rf PyMesaHandler
git clone --recurse-submodules https://github.com/gautam-404/PyMesaHandler.git
cd PyMesaHandler
pip install -r requirements.txt
pip install .