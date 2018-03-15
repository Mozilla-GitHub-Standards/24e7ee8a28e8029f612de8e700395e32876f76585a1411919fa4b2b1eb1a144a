#!/bin/bash

# Retrieves the URLs of all harvester runs so far.
# Downloads and extracts the artifacts. 

# IMPORTANT: Extracted logfiles are big, e.g. ~3.5 gB per run. (Not anymore. Only first ~10)
if [[ "$1" = ""  ]]
then
  echo "Please enter Start date for artifact download."
  echo "Date format 'YYYY-MM-DD'"
  echo "  ./data_collection [start date (incl.)] [end date (excl.), opt.]"
  exit 1
fi

START=$1

if [[ "$2" = ""  ]]
then
  END="2020-12-31"
else  
  END=$2
fi

node main.js $START $END > urls.txt

sed -i '/got tasks.../d' urls.txt
WORKDIR=$(pwd)
if ! [[ -e "$WORKDIR/data" ]]
then
  mkdir $WORKDIR/data
  touch $WORKDIR/data/history
fi

COUNT=0
for URL in $(cat urls.txt)
do
  if ! grep -Fxq $URL $WORKDIR/data/history
  then
    echo "$URL" >> $WORKDIR/data/history
    echo "$URL"
    mkdir tmp
    cd tmp
    wget "$URL"
    bzip2 -d public%2Fcanarylog.tar.bz2
    tar -xf public%2Fcanarylog.tar
    cd .tlscanary/log/*/*/*
    bzip2 -d log.bz2
    mv $WORKDIR/tmp/.tlscanary/log/*/*/* $WORKDIR/data
    cd $WORKDIR
    rm -rf tmp
  fi
done


rm urls.txt

python database.py $WORKDIR/data/
