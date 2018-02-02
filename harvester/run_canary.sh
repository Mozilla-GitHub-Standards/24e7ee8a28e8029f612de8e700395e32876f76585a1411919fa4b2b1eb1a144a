#!/usr/bin/env bash

tlscanary scan -l 100

cd /home/worker/

mkdir log
mkdir log/
tar -cjf log/canarylog.tar.bz2 .tlscanary/log
