#!/bin/sh
export PYTHONPATH=$PYTHONPATH:../
echo $PYTHONPATH
python -m unittest discover -p "*Test.py"
