//
//  EndView.swift
//  DreamApp Watch App
//
//  Created by Rishabh Mallela on 6/16/23.
//

import SwiftUI

struct EndView: View {
    
    var driver: Driver
    
    var body: some View {
        VStack {
            Text("Good Morning")
                .padding()
            Text("You can check your sleep summary on your phone")
                .padding()
        }
        .navigationBarBackButtonHidden(true)
        .onAppear(perform: start)
        
    }
    
    func start() {
        driver.end()
    }
}

struct EndView_Previews: PreviewProvider {
    static var previews: some View {
        Text("hello world")
    }
}
