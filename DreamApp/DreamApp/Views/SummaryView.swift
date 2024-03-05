//
//  SummaryView.swift
//  DreamApp
//
//  Created by Rishabh Mallela on 6/16/23.
//

import SwiftUI

struct SummaryView: View {
    
    var serverCommunicator: ServerCommunication
    
    var body: some View {
        Text("Sound stimuli was activated \(serverCommunicator.numberOfTimesActivated) times")
            .padding()
            .onAppear(perform: start)
            .navigationBarBackButtonHidden(true)
    }
    
    func start() {
        serverCommunicator.endServer()
    }
}

struct SummaryView_Previews: PreviewProvider {
    static var previews: some View {
        Text("hello world")
    }
}
