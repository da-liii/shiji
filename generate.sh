#!/bin/bash

mkdir build
python3 convert.py
pandoc test.md -o build/shiji.epub
rm -rf test.md
cd build
unzip shiji.epub
rm -rf shiji.epub
python3 ../replace.py
cp ../data/*.* .
cp ../data/META-INF . -R
zip ../shiji.epub * META-INF/*
cd ..
rm -rf build
