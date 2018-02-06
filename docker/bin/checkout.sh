#!/bin/bash

# Clone the repo.
for i in 0 2 5; do
    sleep $i
    # FIXME
    git clone -b taskcluster-proxy-experiments https://github.com/mozilla/canary-harvester.git && break
    rm -rf canary-harvester
done

# Run the harvester script
canary-harvester/harvester/run_canary.sh
