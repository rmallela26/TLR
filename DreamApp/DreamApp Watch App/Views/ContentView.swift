//
//  ContentView.swift
//  DreamApp Watch App
//
//  Created by Rishabh Mallela on 6/14/23.
//

import SwiftUI 
import Foundation

struct ContentView: View {
    
    @ObservedObject private var connectivityManager = WatchConnectivityManager.shared
    
    
    var body: some View {
        NavigationView {
            NavigationLink(destination: SleepView(goingBackToSleep: false)) {
                Text("Sleep")
            }
//            .navigationTitle("Dream Sage")
        }

    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
