//
//  PauseView.swift
//  DreamApp Watch App
//
//  Created by Rishabh Mallela on 6/16/23.
//

import SwiftUI

struct PauseView: View {
    
    var driver: Driver
    
    var body: some View {
        NavigationLink("Resume", destination: SleepView(goingBackToSleep: true)).onAppear(perform: start)
    }
    
    func start() {
        driver.end()
    }
}

struct PauseView_Previews: PreviewProvider {
    static var previews: some View {
        Text("hello world")
    }
}
