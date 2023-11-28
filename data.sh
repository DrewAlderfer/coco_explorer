#!/bin/bash
if [ -d "./finder/static/data" ]; then
    echo "data directory already exists..."
else
    mkdir ./finder/static/data
fi

cd ./finder/static/data
wget http://images.cocodataset.org/zips/train2017.zip http://images.cocodataset.org/annotations/annotations_trainval2017.zip
7z x train2017.zip
7z x annotations_trainval2017.zip
