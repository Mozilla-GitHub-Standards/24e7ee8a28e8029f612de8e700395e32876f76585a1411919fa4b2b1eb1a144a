#!/usr/bin/env bash

# Insert this run into the taskcluster index
# delete the python stuff it doesn't work
# python /home/worker/canary-harvester/harvester/set_index.py
timestamp=$(date +'%Y-%m-%d-%H-%M-%S')
curl -v -X PUT "http://taskcluster/index/v1/task/project.nss-nspr.canary-harvester-test.${timestamp}" -H 'Content-Type: application/json' -d "{\"taskId\":\"${TASK_ID}\", \"rank\":10, \"data\":{}, \"expires\":\"2020-02-06T08:26:21.362Z\"}"

tlscanary scan -l 10000 -m 20 -f 0 

cd /home/worker/

mkdir log
mkdir log/
tar -cjf log/canarylog.tar.bz2 .tlscanary/log
