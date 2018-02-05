#!/bin/bash

# Clone the repo.
for i in 0 2 5; do
    sleep $i
    git clone https://github.com/mozilla/canary-harvester.git && break
    rm -rf canary-harvester
done

# Run the harvester script
# canary-harvester/harvester/run_canary.sh

# FIXME: REMOVE AGAIN
python /home/worker/bin/set_index.py

tlscanary scan -l 100

cd /home/worker/

mkdir log
mkdir log/
tar -cjf log/canarylog.tar.bz2 .tlscanary/log

