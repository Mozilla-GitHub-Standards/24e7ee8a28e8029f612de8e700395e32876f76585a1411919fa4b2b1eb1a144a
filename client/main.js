var taskcluster = require('taskcluster-client');

var index = new taskcluster.Index();
// var namespaces = index.listNamespaces("docker.images.v1.nss.fuzz",
//                                       {limit: 10});

// namespaces.then(function(result){
//     console.log("namespaces result: " + JSON.stringify(result));
// }, function(error) {
//     console.log("namespaces error: " + error);
// });

var tasks = index.listTasks("index.project.nss-nspr.canary-harvester",
                            {limit: 10});

tasks.then(function(result){
    console.log("tasks result: " + JSON.stringify(result));
    console.log("got tasks ...");
    let continuationToken = result.continuationToken;
    let tasks = result.tasks;
    let queue = new taskcluster.Queue();
    for (var i = 0; i < tasks.length; i++) {
        let taskObject = tasks[i];
        let artifact = queue.getLatestArtifact(taskObject.taskId, "public/image.tar");
        artifact.then(function(result){
            console.log("artifact result: " + JSON.stringify(result));
        }, function(error) {
            console.log("artifact error: " + error);
        });
    }
}, function(error) {
    console.log("tasks error: " + error);
});

// var task = index.findTask("tc-treeherder.v2.nss-try.d34685e75f62cf220a7749458481a4fc1cdfe443.3000");

// task.then(function(result){
//     console.log("task result: " + result);
// }, function(error) {
//     console.log("task error: " + error);
// });

