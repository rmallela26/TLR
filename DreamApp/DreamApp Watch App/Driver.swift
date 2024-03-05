//
//  Driver.swift
//  DreamApp Watch App
//
//  Created by Rishabh Mallela on 6/15/23.
//
//  Will drive the bulk of the program/processing. Will be controlled by Main

import WatchKit
import Foundation

class Driver: NSObject {
    
//    @ObservedObject private var connectivityManager = WatchConnectivityManager.shared
    private var workoutManager = WorkoutManager()
    private var motionManager = MotionManager()
    private var timer: Timer?
    
    func start() {
        //manage data collection, data gathering, watch connectivity here
        workoutManager.requestAuthorization()
        workoutManager.startWorkout()
        motionManager.startAccelerometers()
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 5, execute: {
            WKInterfaceDevice.current().enableWaterLock()
            print(WKInterfaceDevice.current().isWaterLockEnabled)
        })
        
        var lastHREMA: Double = -1
        var hrEMAs: [Double] = []
        var avgHR: Double?
        var motionData: [[Double]]?
        let alpha = 0.95
        var epochCounter = 0
        var hrFeature: Double?
        var heartRates: [Double]?
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 30, execute: {
            self.timer = Timer(fire: Date(), interval: (30), repeats: true, block: { (timer) in
                heartRates = self.workoutManager.getHRs()
                avgHR = self.workoutManager.getAvgHR()
                motionData = self.motionManager.getMotionData()
                
                print(motionData!)
                print(avgHR!)
                print(heartRates!)
                
                //calculate hr ema
                if (lastHREMA == -1) { //first reading
                    lastHREMA = avgHR!
                    hrEMAs.append(avgHR!)
                } else {
                    let hrEMA = (1 - alpha) * avgHR! + alpha * lastHREMA
                    hrEMAs.append(hrEMA)
                    lastHREMA = hrEMA
                }
                
                if (epochCounter < 14) {
                    hrFeature = Double(hrEMAs[epochCounter]/1000.0)
                } else {
                    let temp = (hrEMAs[epochCounter]-hrEMAs[epochCounter-8])
                    hrFeature = Double(pow(temp, 3)/1000.0)
                }
                
                print(hrFeature!)
                
                if (hrFeature!.isNaN) {
                    //restart all hr
                    hrFeature = 0
                    lastHREMA = -1
                    epochCounter = -1
                    hrEMAs = []
                }
                
                //open watch connectivity session and send hr feature and motion data
                WatchConnectivityManager.shared.send(motionData ?? [[]], hrFeature ?? 0, heartRates ?? [])
                
                epochCounter += 1
                
            })

            RunLoop.current.add(self.timer!, forMode: RunLoop.Mode.default)
        })
        
        
        
    }
    
    func pause() { //TO BE ABLE TO USE THIS BUTTON, NEED TO SAVE DATE() WHEN PAUSED, AND THEN ADD A SUBTRACTION FEATURE IN MOTIN MANAGER TO SUBTRACT AWAY THE DIFFERENCE IN TIME
        //pause everything
    }
    
    func end() {
        self.timer?.invalidate()
        workoutManager.endWorkout()
        motionManager.stopAccelerometers()
    }

}
