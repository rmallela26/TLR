//
//  ContentView.swift
//  DreamApp
//
//  Created by Rishabh Mallela on 6/14/23.
//

import SwiftUI
import UIKit

struct ContentView: View {
    
    
    var body: some View {
        
        NavigationView {
            NavigationLink(destination: SleepView()) {
                Text("Press here when ready to sleep. After pressing, open watch app and press sleep").padding()
            }
        }
        .navigationTitle("Dream")
        
    }

}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
