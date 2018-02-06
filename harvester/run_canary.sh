#!/usr/bin/env bash

# Insert this run into the taskcluster index
python /home/worker/bin/set_index.py

tlscanary scan -l 100

cd /home/worker/

mkdir log
mkdir log/
tar -cjf log/canarylog.tar.bz2 .tlscanary/log
