#!/bin/bash

# Retrieves the URLs of all harvester runs so far.
# Downloads and extracts the artifacts. 

# IMPORTANT: Extracted logfiles are big, e.g. ~3.5 gB per run.
if [[ "$1" = ""  ]] || [[ "$2" = ""  ]]
then
  echo "Please enter Start AND End Index for URLs to download."
  echo "  ./data_collection [first URL #] [last URL #]"
  exit 1
fi

node main.js > urls.txt

sed -i '/got tasks.../d' urls.txt
WORKDIR=$(pwd)
if ! [[ -e "$WORKDIR/data" ]]
then
  mkdir $WORKDIR/data
fi

COUNT=0
MIN=$(($1-1))
MAX=$2
for URL in $(cat urls.txt)
do
  if [[ $COUNT -gt $MAX ]]
  then
    break
  fi
  # Starts at third URL because first two are test runs without artifacts.
  # TODO: Choice of runs to download should be made variable.
  
  if [[ $COUNT -gt $MIN ]] 
  then
    echo "$URL"
    mkdir tmp
    cd tmp
    wget "$URL"
    bzip2 -d public%2Fcanarylog.tar.bz2
    tar -xf public%2Fcanarylog.tar
    cd .tlscanary/log/*/*/*
    bzip2 -d log.bz2
    mv $WORKDIR/temp/.tlscanary/log/*/* $WORKDIR/data
    cd $WORKDIR
    rm -rf tmp
  fi
  COUNT=$(($COUNT+1))
done

rm urls.txt
