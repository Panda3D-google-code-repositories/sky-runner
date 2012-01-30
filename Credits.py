from pandac.PandaModules import *

from direct.showbase import DirectObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage

from GameStates import State

class Credits(DirectObject.DirectObject):  
    def __init__( self, skyRunner ): 
        self.skyRunnerInstance = skyRunner
        #self.frame2 = DirectFrame(frameSize=(-0.5,0.5,-0.5,0.5), parent=render2d, image="hud.Sources/TitleScreen.jpg", sortOrder=(-1))
        self.frame = OnscreenImage(image = "hud.Sources/credits3.png",pos=(0, 0, 0),scale = (1.0,0.46,0.46))#DirectFrame(frameSize=(-0.5, 0.5, -0.5, 0.5), frameColor=(0.8,0.8,0.8,0), pos=(0,0,0),image="hud.Sources/credits.png")
        self.frame.setTransparency(TransparencyAttrib.MAlpha)
        
      
        
        
        mapsCredits = loader.loadModel('hud.Sources/mainMenu/buttons_back_maps.egg')
        self.backButton = DirectButton(parent=self.frame,pos=(0.8,0,-0.8),image = (mapsCredits.find('**/backready'),
                         mapsCredits.find('**/backclicked'),
                         mapsCredits.find('**/backrollover'),
                         mapsCredits.find('**/backdisable')),command=self.hide, scale=(0.23,0.5,0.5),
                         borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06),  
                         frameColor=(0.8,0.8,0.8,0),rolloverSound=self.skyRunnerInstance.soundManager.over,clickSound=self.skyRunnerInstance.soundManager.click)

        self.show()   
    def show(self): #Function that display the window
        self.frame.show()
    def hide(self): #Function that hide the window
        if self.skyRunnerInstance.gameState == State.INGAMECREDITSMENU:
            self.skyRunnerInstance.gameState = State.INGAMEMENU
            
        if self.skyRunnerInstance.gameState == State.CREDITSMENU:
            self.skyRunnerInstance.gameState = State.MAINMENU
        
        
        
        self.frame.hide()