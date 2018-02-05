#!/usr/bin/python

import taskcluster
import os

index = taskcluster.Index({
    'credentials': {},
    'baseUrl': "http://taskcluster/index"})

now = taskcluster.fromNow("0 seconds").strftime('%Y-%m-%d-%H-%M-%S')
taskId = os.environ["TASK_ID"]
namespace = "index.project.nss-nspr.canary-harvester-test." + now
payload = {
    "taskId": taskId,
    "rank": 0,
    "data": {"desc": "canary harvester test"},
    "expires": '2018-02-08T08:26:21.362Z'
}
index.insertTask(namespace, payload)
