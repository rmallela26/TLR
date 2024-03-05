//
//  ServerCommunication.swift
//  DreamApp
//
//  Created by Rishabh Mallela on 6/16/23.
//

import UIKit

struct Data: Codable, Identifiable {
    var id = UUID().uuidString
    var hr: Double
    var time: Int
    var lastEMA: Double
    var motionData: [[Double]]
    var heartRates: [Double]
}

class ServerCommunication: NSObject {
    
    var startTime: [Double] = []
    init(date: Date) {
        super.init()
        startTime = dateToDouble(date: date)
    }
    
    var lastMotionEMA: Double = -1
    var stimulusActivator = StimulusActivation()
    var completeMotionData: [[Double]] = []
    var numberOfTimesActivated = 0
    var numInRow = 0
    var myData = Data(hr: 0, time: 0, lastEMA: 0, motionData: [[]], heartRates: [])
    var done = false
    var cuedTimes: [[Double]] = []
    
    func sendDataToServer(motionData: [[Double]], hrFeat: Double, time: Int, heartRates: [Double]) {
        
        if (done) {
            return
        }
        
        myData.hr = hrFeat
        myData.time = time
        myData.lastEMA = lastMotionEMA
        myData.motionData = motionData
        myData.heartRates = heartRates
        
        guard let uploadData = try? JSONEncoder().encode(myData) else {
            print("Couldn't do JSON Encoder")
            return
        }
        
        
        let url = URL(string: "http://34.102.41.199")! //http://192.168.1.68:8080 http://34.102.41.199
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let task = URLSession.shared.uploadTask(with: request, from: uploadData) { data, response, error in
            if let error = error {
                print ("error: \(error)")
                return
            }
            guard let response = response as? HTTPURLResponse,
                (200...299).contains(response.statusCode) else {
                print ("server error")
                return
            }
            if let mimeType = response.mimeType,
                mimeType == "application/json",
                let data = data,
//                let dataString = String(data: data, encoding: .utf8),
//                print ("got data: \(dataString)")
                let jsonObject = try? JSONSerialization.jsonObject(with: data, options: []),
               let jsonDict = jsonObject as? [String: String] {
                
                
                    let isREM = jsonDict["rem"] ?? "0"
                    self.lastMotionEMA = Double(jsonDict["ema"] ?? String(self.lastMotionEMA))!
                    print(isREM)
                    
                    if (isREM == "1") {
                        self.numInRow += 1
                        if (self.numInRow <= 4) {
                            self.numberOfTimesActivated += 1
                            self.stimulusActivator.activateStimuli()
                            self.cuedTimes.append(self.dateToDouble(date: Date()))
                        }
                    } else {
                        self.numInRow = 0
                        print("not rem")
                    }
            }
        }
        task.resume()
        print("done")
        
    }
    
    func endServer() {
        print(cuedTimes)
        print(startTime)
        sendDataToServer(motionData: cuedTimes, hrFeat: myData.hr, time: -1, heartRates: startTime) //send the times of when it was cued in motionData variable, and send start time in heartRates variable
        done = true
    }
    
    func dateToDouble(date: Date) -> [Double] {
        let formatter = DateFormatter()
        formatter.dateFormat = "YY,MM,d,HH,mm,ss"
        let datestr = formatter.string(from: date)
        let arr = datestr.components(separatedBy: ",")
        
        var newArr: [Double] = []
        var i = 0
        while(i < arr.count) {
            newArr.append(Double(arr[i])!)
            i += 1
        }
        
        return newArr
    }

}







