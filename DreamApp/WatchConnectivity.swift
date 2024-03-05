//
//  WatchConnectivity.swift
//  DreamApp
//
//  Created by Rishabh Mallela on 6/14/23.
//

import UIKit
import WatchConnectivity

struct NotificationMessage {
    let motionData: [[Double]]
    let hrFeature: Double
    let heartRates: [Double]
}


final class WatchConnectivityManager: NSObject, ObservableObject {
    static let shared = WatchConnectivityManager()
    @Published var notificationMessage: NotificationMessage? = nil
    var gotData = false
    
    private override init() {
        super.init()
        
        if WCSession.isSupported() {
            WCSession.default.delegate = self
            WCSession.default.activate()
        }
    }
    
    private let mMessageKey = "motion"
    private let hMessageKey = "heart rate"
    private let sMessageKey = "hrs"
    
    func send(_ motion: [[Double]], _ heart: Double, _ rates: [Double]) {
        print("sending")
        guard WCSession.default.activationState == .activated else {
          return
        }
        #if os(iOS)
        guard WCSession.default.isWatchAppInstalled else {
            return
        }
        #else
        guard WCSession.default.isCompanionAppInstalled else {
            return
        }
        #endif
        
        WCSession.default.sendMessage([mMessageKey : motion, hMessageKey: heart, sMessageKey: rates], replyHandler: nil) { error in
            print("Cannot send message: \(String(describing: error))")
        }
    }
}

extension WatchConnectivityManager: WCSessionDelegate {
    func session(_ session: WCSession, didReceiveMessage message: [String : Any]) {
        if let motionNotification = message[mMessageKey] as? [[Double]], let heartNotification = message[hMessageKey] as? Double, let ratesNotification = message[sMessageKey] as? [Double] {
            DispatchQueue.main.async { [weak self] in
                self?.notificationMessage = NotificationMessage(motionData: motionNotification, hrFeature: heartNotification, heartRates: ratesNotification)
                self?.gotData = true
            }
        }
        //call data management function
    }
    
    func session(_ session: WCSession,
                 activationDidCompleteWith activationState: WCSessionActivationState,
                 error: Error?) {}
    
    #if os(iOS)
    func sessionDidBecomeInactive(_ session: WCSession) {}
    func sessionDidDeactivate(_ session: WCSession) {
        session.activate()
    }
    #endif
}
