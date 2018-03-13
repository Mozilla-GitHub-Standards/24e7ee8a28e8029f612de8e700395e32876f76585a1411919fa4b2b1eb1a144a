var minDate = Number(new Date("2018-02-08"));

if (process.argv[2] == undefined || process.argv[3] == undefined){
  console.log("Please provide date range for artifact download. Start (including) and End (excluding)")
  return;
}
var startDate = Math.max(Number(new Date(process.argv[2])), minDate);
var endDate = Number(new Date(process.argv[3]));

var taskcluster = require('taskcluster-client');

var index = new taskcluster.Index();

var tasks = index.listTasks("project.nss-nspr.canary-harvester",
                            {limit: 1000});

tasks.then(function(result, reject){
    // console.log("tasks result: " + JSON.stringify(result));
    //console.log("got tasks ...");
    let continuationToken = result.continuationToken;
    let tasks = result.tasks;
    let queue = new taskcluster.Queue();
    for (var i = 0; i < tasks.length; i++) {
        let taskObject = tasks[i];
        let taskDate = Number(new Date(taskObject.namespace.substr(taskObject.namespace.indexOf(".20")+1, 10)));
        if (taskDate >= startDate && taskDate < endDate){
          let artifact = queue.buildUrl(queue.getLatestArtifact, taskObject.taskId, "public/canarylog.tar.bz2");
          console.log(artifact);
        }
    }
}, function(error) {
    console.log("tasks error: " + error);
});
