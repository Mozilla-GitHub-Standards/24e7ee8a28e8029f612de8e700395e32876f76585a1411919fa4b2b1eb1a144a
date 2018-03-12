#!/bin/bash

# Retrieves the URLs of all harvester runs so far.
# Downloads and extracts the artifacts. 

# IMPORTANT: Extracted logfiles are big, e.g. ~3.5 gB per run. (Not anymore. Only first ~10)
if [[ "$1" = ""  ]] || [[ "$2" = ""  ]]
then
  echo "Please enter Start AND End date for artifact download."
  echo "Date format 'YYYY-MM-DD'"
  echo "  ./data_collection [start date (incl.)] [end date (excl.)]"
  exit 1
fi

node main.js $1 $2 > urls.txt

sed -i '/got tasks.../d' urls.txt
WORKDIR=$(pwd)
if ! [[ -e "$WORKDIR/data" ]]
then
  mkdir $WORKDIR/data
fi

COUNT=0
for URL in $(cat urls.txt)
do
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
done

rm urls.txt
