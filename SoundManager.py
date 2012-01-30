class SoundManager( object ):
    def __init__( self ):
        self.soundWalking = base.loader.loadSfx("sounds.Sources/walkingNoiseFree.wav")
        self.soundWalking.setLoop(True)
        self.soundWalking.setVolume(0.0)  
        #self.soundWalking.play()
        
        self.soundJump = base.loader.loadSfx("sounds.Sources/jump.wav")
        self.soundJump.setLoop(False)
        self.soundJump.setVolume(1.0)
          
        self.soundAmbient = base.loader.loadSfx("sounds.Sources/ambient.wav")
        self.soundAmbient.setLoop(True)
        self.soundAmbient.setVolume(1.0) 
        #self.soundAmbient.play()
        
        self.screamSound = base.loader.loadSfx("sounds.Sources/screamFalling.wav")
        self.screamSound.setVolume(1.0) 
        
        self.click = base.loader.loadSfx("sounds.Sources/buttonClick.wav")
        self.click.setVolume(0.1)
        
        self.over = base.loader.loadSfx("sounds.Sources/buttonOver.wav")
        self.over.setVolume(0.1)
        
        self.sounds = [self.soundWalking,self.soundJump,self.soundAmbient,self.screamSound,self.click,self.over]
        
    def stopAllSounds( self ):
        for sound in self.sounds:
            sound.stop()