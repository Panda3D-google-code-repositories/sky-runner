from pandac.PandaModules import *

from direct.showbase import DirectObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage

from GameStates import State

class Credits(DirectObject.DirectObject):  
    def __init__( self, skyRunner ): 
        self.skyRunnerInstance = skyRunner
        self.frame = DirectFrame(frameSize=(-0.5, 0.5, -0.5, 0.5), frameColor=(0.8,0.8,0.8,.8), pos=(0,0,0))
        self.headline = DirectLabel(parent=self.frame, text="Credits", scale=0.085, frameColor=(0,0,0,0), pos=(0,0,0.4))
        
        self.Text = DirectFrame(
                                      parent=self.frame, 
                                      text="Sky Runner\n\nUniversidade Federal do Rio de Janeiro (UFRJ)\n\n\nAuthors: \nFelipe, Marcos, Renato.", 
                                      scale=0.045, 
                                      frameColor=(0,0,0,0), 
                                      pos=(-0.48,0,0.35),
                                      text_align=TextNode.ALeft)
        
        self.backButton = DirectButton(parent=self.frame, text="back", command=self.hide, 
                            pos=(0,0,-0.4), text_scale=0.08, text_fg=(0,0,0,1), text_align=TextNode.ACenter, 
                            borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06), 
                            frameColor=(0.8,0.8,0.8,0), rolloverSound=self.skyRunnerInstance.soundManager.over,clickSound=self.skyRunnerInstance.soundManager.click)

        self.show()   
    def show(self): #Function that display the window
        self.frame.show()
    def hide(self): #Function that hide the window
        if self.skyRunnerInstance.gameState == State.INGAMECREDITSMENU:
            self.skyRunnerInstance.gameState = State.INGAMEMENU
            
        if self.skyRunnerInstance.gameState == State.CREDITSMENU:
            self.skyRunnerInstance.gameState = State.MAINMENU
        
        
        
        self.frame.hide()