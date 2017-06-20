#!/bin/sh
export PYTHONPATH=$PYTHONPATH:../
python3 -m unittest discover -p "*Test.py"
