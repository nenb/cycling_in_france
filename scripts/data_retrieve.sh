#!/bin/bash

# Create soft link to local copy of wind data
ln -s ${DATA_DIR} ../data/raw

# Use L option to deal with redirect issue for data
curl -Lo ../data/raw/gadm36_FRA_gpkg.zip https://biogeo.ucdavis.edu/data/gadm3.6/gpkg/gadm36_FRA_gpkg.zip

unzip ../data/raw/gadm36_FRA_gpkg.zip -d ../data/raw

# Clean-up
rm ../data/raw/gadm36_FRA_gpkg.zip
