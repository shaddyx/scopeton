#!/bin/bash

pushd ../
rm -rf dist
python setup.py sdist
#twine register dist/* -r pypi
twine upload dist/*
popd