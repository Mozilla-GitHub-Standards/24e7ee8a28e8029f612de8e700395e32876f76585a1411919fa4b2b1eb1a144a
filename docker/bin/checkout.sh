#!/bin/bash

# Clone the repo.
for i in 0 2 5; do
    sleep $i
    git clone https://github.com/mozilla/canary-harvester.git && exit 0
    rm -rf canary-harvester
done

# Run the harvester script
canary-harvester/harvester/run_canary.sh
