//
//  SoundPlayer.swift
//  DreamApp
//
//  Created by Rishabh Mallela on 6/16/23.
//

import Foundation
import AVFoundation

class SoundPlayer {
    var audioPlayer: AVAudioPlayer?
    let sound: String
    let type: String
    
    init() {
        sound = "Morse Code Audio File"
        type = "m4a"
        if let path = Bundle.main.path(forResource: sound, ofType: type) {
            do {
                audioPlayer = try AVAudioPlayer(contentsOf: URL(fileURLWithPath: path))
            } catch {
                print("couldn't play the sound")
            }
        }
    }
    
    init(rand: Int) {
        sound = "TLR Training Recording"
        type = "m4a"
        if let path = Bundle.main.path(forResource: sound, ofType: type) {
            do {
                audioPlayer = try AVAudioPlayer(contentsOf: URL(fileURLWithPath: path))
            } catch {
                print("couldn't play the sound")
            }
        }
    }
    
    func playSound() {
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default)
            try AVAudioSession.sharedInstance().setActive(true)
            if let path = Bundle.main.path(forResource: sound, ofType: type) {
                audioPlayer = try AVAudioPlayer(contentsOf: URL(fileURLWithPath: path))
                audioPlayer?.play()
            }
        } catch {
            print("couldn't play the sound")
        }
    }
}
