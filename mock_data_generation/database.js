const sqlite3 = require('sqlite3').verbose();
var Promise = require('bluebird');
var Car = require('./cars');
var Event = require('./events');
var db;
// open database in memory
function openDB(){
    db = new sqlite3.Database('./db/data.db', (err) => {
        if (err) {
          return console.error(err.message);
        }
        console.log('Connected to the SQlite database.');
    });
}
openDB();

db.serialize(function() {
    // db.run("DROP TABLE cars");
    // db.run("DROP TABLE events");
    db.run("CREATE TABLE IF NOT EXISTS cars(id Int PRIMARY KEY, empty Int, commodity varchar, carType varchar,referenceNum varchar, status varchar, eta Int)");
    db.run("CREATE TABLE IF NOT EXISTS events(carId Int, name varchar, dateTime Int, city varchar, state varchar, type varchar, FOREIGN KEY(carId) REFERENCES cars(id))");
    
});



module.exports = class dbConnection{
    constructor(){
        this.selectSQL = "SELECT c.id as id, c.empty as empty, c.commodity as commodity, c.carType as carType, c.referenceNum, c.status as status, c.eta as eta, e.name as name, e.dateTime as dateTime, e.city as city, e.state as state, e.type as type"
        + " FROM cars as c INNER JOIN events as e on c.id = e.carId ";
    }
    insertCars(cars){
        var stmt = db.prepare("INSERT INTO cars values(?, ?, ?, ?, ?, ?, ?)");
        var eventStmt = db.prepare("INSERT INTO events values(?, ?, ?, ?, ?, ?)");
        cars.forEach((car)=>{
            stmt.run(car.id, car.empty == 'true'?1:0, car.commodity, car.carType, car.serviceIssue.referenceNumber, car.serviceIssue.status, car.eta.getTime());
            car.completedEvents.forEach((event)=>{
                console.log(event);
                eventStmt.run(event.carId, event.name, event.dateTime.getTime(), event.location.city, event.location.state, event.type);
            });
            car.scheduledEvents.forEach((event)=>{
                console.log(event);
                eventStmt.run(event.carId, event.name, event.dateTime.getTime(), event.location.city, event.location.state, event.type);
            });
        });

        stmt.finalize(()=>{
        });
    }

    getAll(){
        return new Promise((resolve, reject) => {
            var data = [];
            //id Int PRIMARY KEY, empty Int, commodity varchar, carType varchar,referenceNumber varchar, status varchar, eta Int
            //carId Int, name varchar, dateTime Int, city varchar, state varchar, type varchar, FOREIGN KEY(carId) REFERENCES cars(id))
            db.all(this.selectSQL, function(err, rows) {
                    formatCars(rows, data);
                    resolve(data);
            })
              
        });
            
    }
    findById(id){
        return new Promise((resolve, reject) =>{
            var data = [];
            db.all(this.selectSQL + "WHERE c.id = '" + id + "'", (err, rows)=>{
                formatCars(rows, data);
                resolve(data[0]);
            });
        })
    }
}
        
//SELECT c.id as id, c.empty as empty, c.commodity as commodity, c.carType as carType, c.referenceNum, c.status as status, e.name as name, e.dateTime as dateTime, e.city as city, e.state as state, e.type as type FROM cars as c INNER JOIN events as e on c.id = e.carId;


function formatCars(rows, data){
    var id;
    var oldId = 1;
    var car = new Car();
    rows.forEach((row) =>{
        id = row.id;
        if(oldId == id){
            let event = new Event();
            event.name = row.name;
            event.dateTime = new Date(row.dateTime);
            event.location.city = row.city;
            event.location.state = row.state;
            if(row.type == "Completed"){
               car.completedEvents.push(event); 
            }
            else{
                car.scheduledEvents.push(event);
            }
        }else{
            if(oldId != 1){
                data.push(car);
            }
            car = new Car();
            car.id = row.id;
            car.commodity = row.commodity;
            car.carType = row.carType;
            car.serviceIssue.referenceNumber = row.referenceNum;
            car.serviceIssue.status = row.status;
            car.eta = new Date(row.eta);
        }
        oldId = id;
    });
    data.push(car);
}



function closeConnection(){
    db.close((err) => {
        if (err) {
            return console.error(err.message);
        }
        console.log('Close the database connection.');
    });
}