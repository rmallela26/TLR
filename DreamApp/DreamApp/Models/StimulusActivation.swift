//
//  StimulusActivation.swift
//  DreamApp
//
//  Created by Rishabh Mallela on 6/16/23.
//

import UIKit

class StimulusActivation: NSObject {
    
    var soundPlayer = SoundPlayer()
    
    func activateStimuli() {
        //activate stimuli (call sound player)
        soundPlayer.playSound()
        print("Activating stimuli")
    }

}
