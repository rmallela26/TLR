//
//  MotionManager.swift
//  DreamApp Watch App
//
//  Created by Rishabh Mallela on 6/14/23.
//

import UIKit
import CoreMotion

class MotionManager: NSObject, ObservableObject {
    
    var motion = CMMotionManager()
    var timer: Timer?
    var motionData = [[Double]]()
    
    func startAccelerometers() {
       // Make sure the accelerometer hardware is available.
       if self.motion.isAccelerometerAvailable {
          self.motion.accelerometerUpdateInterval = 1.0 / 30.0  // 30 Hz
          self.motion.startAccelerometerUpdates()


          // Configure a timer to fetch the data.
          let beginning = Date()
          var counter = 1
          
          self.timer = Timer(fire: Date(), interval: (1.0/30.0), //30 Hz 1.0/30.0
                repeats: true, block: { (timer) in
             // Get the accelerometer data.

             if let data = self.motion.accelerometerData {
                var subarray = [Double]()
                 subarray.append(CFDateGetTimeIntervalSinceDate(Date() as CFDate, beginning as CFDate))
                 subarray.append(data.acceleration.x)
                 subarray.append(data.acceleration.y)
                 subarray.append(data.acceleration.z)
                 self.motionData.append(subarray)
//                 print(counter, self.motionData.last!)
                 counter += 1
                
             }
          })


          // Add the timer to the current run loop.
           RunLoop.current.add(self.timer!, forMode: RunLoop.Mode.default)
       }
    }
    
    func stopAccelerometers() {
        motion.stopAccelerometerUpdates()
        self.timer?.invalidate()
    }
    
    func getMotionData() -> [[Double]] {
        let temp = motionData
        motionData = [[Double]]() //clear it
        return temp
    }
}
