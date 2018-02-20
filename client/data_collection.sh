#!/bin/bash

# Retieves the URLs of all harvester runs so far.
# Downloads and extracts the artifacts. 

# IMPORTANT: Extracted logfiles are big, e.g. ~3.5 gB per run.

node main.js > urls.txt

sed -i '/got tasks.../d' urls.txt
WORKDIR=$(pwd)
mkdir $WORKDIR/data

COUNT=0
for URL in $(cat urls.txt)
do
  
  # Starts at third URL because first two are test runs without artifacts.
  # TODO: Choice of runs to download should be made variable.
  
  if [ $COUNT -gt 1 ]
  then
    echo "$URL"
    mkdir tmp
    cd tmp
    wget "$URL"
    bzip2 -d public%2Fcanarylog.tar.bz2
    tar -xf public%2Fcanarylog.tar
    cd .tlscanary/log/*/*/*
    bzip2 -d log.bz2
    cd ..
    mv ./* $WORKDIR/data
    cd $WORKDIR
    rm -rf tmp
  fi
  COUNT=$(($COUNT+1))
done

rm urls.txt
