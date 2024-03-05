//
//  SleepView.swift
//  DreamApp
//
//  Created by Rishabh Mallela on 6/17/23.
//

import SwiftUI

struct SleepView: View {
    
    var serverCommunicator = ServerCommunication(date: Date())
    var soundPlayer = SoundPlayer(rand: 5)
    @ObservedObject private var connectivityManager = WatchConnectivityManager.shared
    @State var sending = "Waiting for connection"
    
    var body: some View {
        VStack {
            Button {
                soundPlayer.playSound()
            } label: {
                Text("Training Audio")
            }.padding()

            NavigationLink(destination: SummaryView(serverCommunicator: serverCommunicator)) {
                Text("Press here when done sleeping to see sleep summary").padding()
            }.navigationBarBackButtonHidden(true)
            
            Text("\(sending)")
        }.onAppear(perform: start)
        
    }
    
    func start() {
        UIApplication.shared.isIdleTimerDisabled = true
        var motionData: [[Double]]?
        var hrFeature: Double?
        var heartRates: [Double]?
        var time = 30
        
        let timer = Timer(fire: Date(), interval: (1), repeats: true, block: { (timer) in
            if (connectivityManager.gotData) {
                connectivityManager.gotData = false
                
                if let md = $connectivityManager.notificationMessage.wrappedValue?.motionData as? [[Double]], let hf = $connectivityManager.notificationMessage.wrappedValue?.hrFeature as? Double, let rt = $connectivityManager.notificationMessage.wrappedValue?.heartRates as? [Double] {
                    motionData = md
                    hrFeature = hf
                    heartRates = rt
                    print(motionData!)
                    print(hrFeature!)
                    print(heartRates!)
                    
                    self.sending = "Running"
                    serverCommunicator.sendDataToServer(motionData: motionData!, hrFeat: hrFeature!, time: time, heartRates: heartRates!)
                    
                }
                time += 30
                
                
                
            } else {
                print(connectivityManager.gotData)
            }
        })

        RunLoop.current.add(timer, forMode: RunLoop.Mode.default)

    }
}

struct SleepView_Previews: PreviewProvider {
    static var previews: some View {
        SleepView()
    }
}
