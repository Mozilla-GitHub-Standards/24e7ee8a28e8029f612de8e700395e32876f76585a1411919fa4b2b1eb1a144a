var taskcluster = require('taskcluster-client');

var index = new taskcluster.Index();

var tasks = index.listTasks("project.nss-nspr.canary-harvester",
                            {limit: 100});

tasks.then(function(result, reject){
    // console.log("tasks result: " + JSON.stringify(result));
    console.log("got tasks ...");
    let continuationToken = result.continuationToken;
    let tasks = result.tasks;
    let queue = new taskcluster.Queue();
    for (var i = 0; i < tasks.length; i++) {
        let taskObject = tasks[i];
        let artifact = queue.buildUrl(queue.getLatestArtifact, taskObject.taskId, "public/canarylog.tar.bz2");
        console.log(artifact);
    }
}, function(error) {
    console.log("tasks error: " + error);
});
