let db_name = "Basic Scenario";
db.getCollection(db_name).drop();
let foundFiles = db.fs.files.find({scenario_name: db_name}, {_id: 1}).map(function (f) {return f._id}).toArray();
let forDeleting = db.fs.chunks.find({files_id: {$in: foundFiles}}, {_id: 1}).map(function (f) {return f._id}).toArray();
db.fs.chunks.deleteMany({_id: { $in: forDeleting}});
db.fs.files.deleteMany({scenario_name: db_name});