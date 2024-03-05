//
//  SleepView.swift
//  DreamApp Watch App
//
//  Created by Rishabh Mallela on 6/14/23.
//

import SwiftUI
import Foundation
import WatchKit

struct SleepView: View { 
    
//    var workoutManager = WorkoutManager()
//    var motionManager = MotionManager()
    var goingBackToSleep: Bool
    var driver = Driver()
    
    var body: some View {
        VStack {
            
//            NavigationLink(destination: PauseView(driver: driver)) {
//                Text("Pause").padding()
//            };
            
            NavigationLink(destination: EndView(driver: driver)) {
                Text("End").padding()
            }.navigationBarBackButtonHidden(true)
            
//            Button {
//                //add functionality to pause sleep (for when people wake up in middle of the night)
//            } label: {
//                Text("Pause")
//            }.padding()
//            Button {
//                //add functionality to end sleep
//                driver.end()
//            } label: {
//                Text("Woke up")
//            }.padding()
        }.onAppear(perform: start)
        

    }
    
    func start() {
        //if going back to sleep, give the person 3 minutes to get back to sleep before checking for rems
        if (goingBackToSleep) {
            DispatchQueue.main.asyncAfter(deadline: .now() + 180, execute: {
                driver.start()
            })
        } else {
            driver.start()
        }
        
        
        
//        print("starting accelerometers")
//        self.motionManager.startAccelerometers()
//        print("")
//        self.workoutManager.requestAuthorization()
//        self.workoutManager.startWorkout()
        
//        var timer = Timer(fire: Date(), interval: (1), repeats: true, block: { (timer) in
//            print("hello mokam")
//        })
//
//        RunLoop.current.add(timer, forMode: RunLoop.Mode.default)
    }
}

struct SleepView_Previews: PreviewProvider {
    static var previews: some View {
        SleepView(goingBackToSleep: false)
    }
}
