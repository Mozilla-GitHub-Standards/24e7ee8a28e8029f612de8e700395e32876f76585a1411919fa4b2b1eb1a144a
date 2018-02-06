#!/usr/bin/env bash

# Insert this run into the taskcluster index
python /home/worker/canary-harvester/harvester/set_index.py
curl -v -X PUT "http://taskcluster/index/v1/task/project.nss-nspr.canary-harvester-test.foo-test" -H 'Content-Type: application/json' -d "{\"taskId\":\"${TASK_ID}\", \"rank\":10, \"data\":{}, \"expires\":\"2019-02-05T17:12:45.495Z\"}"

tlscanary scan -l 100

cd /home/worker/

mkdir log
mkdir log/
tar -cjf log/canarylog.tar.bz2 .tlscanary/log
