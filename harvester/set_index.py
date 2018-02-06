#!/usr/bin/python

import taskcluster
import os

index = taskcluster.Index({'baseUrl': 'http://taskcluster/index'})
queue = taskcluster.Queue()

# TESTING
ns = index.listNamespaces('project.nss-nspr.canary-harvester-test', {})
print('namespaces: ' + str(ns))

now = taskcluster.fromNow("0 seconds").strftime('%Y-%m-%d-%H-%M-%S')
taskId = os.environ["TASK_ID"]
namespace = "index.project.nss-nspr.canary-harvester-test." + now
task = queue.task(taskId)
print(str(task))
payload = {
    "taskId": taskId,
    "rank": 0,
    "data": {"desc": "canary harvester test"},
    "expires": task["expires"]
}
#index.insertTask(namespace, payload)
