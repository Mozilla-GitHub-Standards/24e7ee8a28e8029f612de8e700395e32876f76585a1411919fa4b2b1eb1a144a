var taskcluster = require("taskcluster-client");

//console.log('hello world');

var index = new taskcluster.Index();

index.ping();

var task = index.findTask('index.docker.images.v1.nss-try.*');

task.then(function(value) {
  console.log(value);
  // expected output: Array [1, 2, 3]
}, function(value) {
  console.log(value);
});



console.log("blabla");
//console.log(task);

//var artifact = index.findArtifactFromTask('Index.public','canarylog.tar.bz2');


//var {taskId} = await index.findTask('docker.images.v1');
