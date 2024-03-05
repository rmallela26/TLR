// const express = require('express');
// const fs = require('fs')
// const app = express();
// const {spawn} = require('child_process');

// app.get('/', (req, res) => {
//   console.log('Hello world received a request.');

//   const python = spawn('python3', ['./practice.py']); //call python program
//   python.on('close', (code) => {
//     // const target = process.env.TARGET || 'World';
//     // res.send(`Hello ${target}!`);
//     const num = fs.readFileSync('face.txt', 'utf8');
//     res.send(`Your random number is ${num}`);
//   });
//     // const num = fs.readFileSync('face.txt', 'utf8');
//     // res.send(`Your random number is ${num}`);
// });

// const port = process.env.PORT || 8080;
// app.listen(port, () => {
//   console.log('Hello world listening on port', port);
// });



const express = require('express')
const {spawn} = require('child_process')
const fs = require('fs')
const fsPromises = require('fs').promises
const { v4: uuidv4 } = require('uuid');

const queueFile = 'answerID.txt';
// let queueGood = true

// function enqueue(element) {
//     fs.appendFileSync(queueFile, element + '\n');
//     return true
// }
  
function dequeue() {
    const data = fs.readFileSync(queueFile, 'utf8');
    const lines = data.trim().split('\n');

    if (lines.length === 0) {
        return null; // Queue is empty
    }

    // let topLine;
    // let remainingLines;
    // if (lines[0] == "\n") {
    //     console.log("MOK MOK MOK MOK MOK MOK MOK MOK MOK")
    //     topLine = lines[1];
    //     remainingLines = lines.slice(2);
    // } else {
    //     topLine = lines[0];
    //     remainingLines = lines.slice(1);
    // }

    const topLine = lines[0];
    const remainingLines = lines.slice(1);

    fs.writeFileSync(queueFile, remainingLines.join('\n'));
    if (remainingLines.length != 0) {
        fs.appendFileSync(queueFile, '\n')
    }

    if (topLine == "") {
        console.log("THINKS THERE IS NO TOP LINE")
        console.log(lines)
        return null;
    }

    return topLine;
}

// function checkFile(file) {
//     if(fs.existsSync(file)) {
//         return true
//     } else {
//         console.log(`waiting for file\nwaiting for file\nwaiting for file\n ${file}`)
//         setTimeout(checkFile(file), 3000);
//     }
    
// }




const app = express()

app.use(express.json({limit: '500mb'}))
app.use(express.urlencoded({limit: '500mb'}))

app.post('/', async (req, res) => {
    const requestId = uuidv4();
    // while(!queueGood) {
    //     console.log("waiting for queue")
    // }
    // queueGood = false
    // queueGood = enqueue(requestId.toString())
    // console.log("enqueued")
    console.log("face face face!")
    //get motion data, hr ema, time in seconds, last motion ema
    const body = req.body
    const uuid = body.id
    
    if (body.time == -1) { //app is done communicating with server, save motion data in persistend volume
        console.log("app is done communicating with server, saving files")
        //write the start time and cued times
        const timesFile = `${uuid}_times.txt`
        let file; 
        file = fs.createWriteStream(timesFile, { flags: 'a' });
        
        file.on('error', function(err) {
            console.log("couldn't save times");
        });
        console.log(body.heartRates);
        console.log(body.motionData);

        file.write(`Start time: ${body.heartRates}\n\nCued times:\n`);
        (body.motionData).forEach((v) => { file.write(v.join(',') + '\n'); });
        file.end();

        file.on('close', function() {
            fs.copyFile(`/usr/src/app/${uuid}_times.txt`, `/usr/src/app/data/finished/${uuid}_times.txt`, (err) => {
                if (err) {
                    console.log("couldn't move times file");
                } else {
                    fs.unlink(`/usr/src/app/${uuid}_times.txt`, (err) => {
                        if (err) console.log("couldn't delete times file on ephemeral storage");
                    });
                }
            });
        });

        fs.copyFile(`/usr/src/app/${uuid}_motion_data.txt`, `/usr/src/app/data/finished/${uuid}_motion_data.txt`, (err) => {
            if (err) {
                console.log("couldn't move motion file");
            } else {
                fs.unlink(`/usr/src/app/${uuid}_motion_data.txt`, (err) => {
                    if (err) console.log("couldn't delete motion file on ephemeral storage");
                });
            }
        });

        fs.copyFile(`/usr/src/app/${uuid}_hr_data.txt`, `/usr/src/app/data/finished/${uuid}_hr_data.txt`, (err) => {
            if (err) {
                console.log("couldn't move hr file");
            } else {
                fs.unlink(`/usr/src/app/${uuid}_hr_data.txt`, (err) => {
                    if (err) console.log("couldn't delete hr file on ephemeral storage");
                });
            }
        });

        fs.copyFile(`/usr/src/app/${uuid}_labels.txt`, `/usr/src/app/data/finished/${uuid}_labels.txt`, (err) => {
            if (err) {
                console.log("couldn't move labels file");
            } else {
                fs.unlink(`/usr/src/app/${uuid}_labels.txt`, (err) => {
                    if (err) console.log("couldn't delete lables file on ephemeral storage");
                });
            }
        });

        res.json({ rem: "saved files", ema: "0" });
        res.send();
        return;        
    } else { //not done do stuff
        //write data to file (motion one file, hr and time another file)
        const motionFile = `${uuid}_motion_data.txt`

        let file;

        //if exists, append, otherwise create new one
        if (fs.existsSync(motionFile)) file = fs.createWriteStream(motionFile, { flags: 'a' });
        else file = fs.createWriteStream(motionFile);

        file.on('error', function(err) { 
            res.json({ rem: "mokington died", ema: "-1"});
            res.send();
            return;
        });
        console.log(body.motionData);
        if (body.motionData == null) {
            res.json({ rem: "mokington died", ema: "-1"});
            res.send();
            return;
        }
        (body.motionData).forEach((v) => { file.write(v.join(',') + '\n'); });
        file.end();

        console.log(body.heartRates)
        const heartRatesFile = `${uuid}_hr_data.txt`;
        const heartRatesLine = JSON.stringify(body.heartRates);

        //if exists, append, otherwise create new one
        if (fs.existsSync(heartRatesFile)) {
            fs.appendFile(heartRatesFile, `${heartRatesLine.slice(1,-1)}\n`, (err) => {
                if (err) {
                    console.log("error ocurred writing heart rates file");
                }
            });
        } else {
            fs.writeFile(heartRatesFile, `${heartRatesLine.slice(1,-1)}\n`, (err) => {
                if (err) {
                    console.log("error ocurred writing heart rates file");
                }
            });
        }

        const othDataFile = `${requestId}_other_data.txt`;
        fs.writeFile(othDataFile, `${body.hr},${body.time},${body.lastEMA}`, (err) => {
            if (err) {
                console.log("error ocurred")
                res.json({ rem: "mokington died", ema: "-1"});
                res.send();
                return;
            }
            

        });

        console.log("done writing to file")
        
        const python = spawn('python3', ['processing.py', requestId.toString(), uuid]) //call python program
        

        python.on('close', (code) => { //anything that i want to run after python code is done running goes here
            console.log(`child process close all stdio with code ${code}`);
            if (code == 1) { //python code crashed
                res.json({ rem: "mokington died", ema: "-1"});
                res.send();
                return;
            }
            // send data to browser
            // let ans;
            // while(!queueGood) console.log("queue is busy")
            // queueGood = false
            // id = dequeue(); 
            // queueGood = true
            const id = dequeue();

            if (id == null) id = requestId
            console.log("dequeued")
            // const answerFile = new File(`${id}_answer.txt`);
            // while(!fs.existsSync(`./${id}_answer.txt`)) console.log(`waiting for file ${id}`)
            // const ans = checkFile(`./${id}_answer.txt`)
            const arr = fs.readFileSync(`${id}_answer.txt`, (err) => {
                if (err) {
                    console.log(`There is no file answer.txt for ${requestId}`);
                    res.json({ rem: "mokington died", ema: "-1"});
                    res.send();
                    return;
                }
            }).toString().split("\n");
            console.log(arr[0])
            console.log(arr[1])
            res.json({ rem: "" + arr[0], ema: "" + arr[1] })
            res.send()

            //delete files
            fs.unlink(`${id}_answer.txt`, (err) => {
                if (err) {
                    console.log("Could not delete file");
                }
            });
            fs.unlink(`${id}_cleaned_motion_data.txt`, (err) => {
                if (err) {
                    console.log("Could not delete file");
                }
            });
            fs.unlink(`${id}_counts.txt`, (err) => {
                if (err) {
                    console.log("Could not delete file");
                }
            });
            fs.unlink(`${id}_other_data.txt`, (err) => {
                if (err) {
                    console.log("Could not delete file");
                }
            });
            console.log("mok mok mok")
            
        });
    }

    
    
})


app.listen(8080, () => console.log('Server listening on port 8080'))

