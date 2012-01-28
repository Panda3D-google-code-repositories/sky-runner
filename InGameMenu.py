import sys

from pandac.PandaModules import *

from direct.showbase import DirectObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage

from Credits import Credits
from GameStates import State


class InGameMenu(DirectObject.DirectObject):
    def __init__( self, skyRunner ):
        self.skyRunnerInstance = skyRunner
        self.frame = DirectFrame(frameSize=(-0.3, 0.3, -0.4, 0.4))
        self.frame['frameColor']=(0.8,0.8,0.8,0.8)

        self.headline = DirectLabel(parent=self.frame, text="Sky Runner", scale=0.085, frameColor=(0,0,0,0), pos=(0,0,0.3))
        
        self.mainMenuButton = DirectButton(parent=self.frame, text="Main Menu", command=self.showMainMenu, pos=(0,0,0.1), text_scale=0.07, text_fg=(0,0,0,1), text_align=TextNode.ACenter, borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06), frameColor=(0.8,0.8,0.8,0))

        #self.creditsButton = DirectButton(parent=self.frame, text="Credits", command=self.showCredits, pos=(0,0,0), text_scale=
        #0.07, text_fg=(0,0,0,1), text_align=TextNode.ACenter, borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06), frameColor=(0.8,0.8,0.8,0))

        maps = loader.loadModel('hud.Sources/mainMenu/buttons_credits_maps.egg')
        self.b = DirectButton(parent=self.frame,pos=(0,0,0),geom = (maps.find('**/creditsready'),
                         maps.find('**/creditsclicked'),
                         maps.find('**/creditsrollover'),
                         maps.find('**/creditsdisable')),command=self.showCredits, scale=0.16)


        self.resumeButton = DirectButton(parent=self.frame, text="Resume", command=self.resumeGame, pos=(0,0,-0.1), text_scale=
        0.07, text_fg=(0,0,0,1), text_align=TextNode.ACenter, borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06),  frameColor=(0.8,0.8,0.8,0))
        
        self.resumeButton = DirectButton(parent=self.frame, text="Exit Game", command=self.endGame, pos=(0,0,-0.2), text_scale=
        0.07, text_fg=(0,0,0,1), text_align=TextNode.ACenter, borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06), frameColor=(0.8,0.8,0.8,0))

        self.show()
        
        self.credits = None
    def show(self): 
        self.frame.show()        
        
    def hide(self): 
        self.frame.hide()
        
    def showMainMenu(self): 
        if self.skyRunnerInstance.gameState == State.INGAMEMENU:
            self.hide()
            self.skyRunnerInstance.game.clearScreenTexts()
            self.skyRunnerInstance.__init__()
        
    def showCredits(self): 
        if self.skyRunnerInstance.gameState == State.INGAMEMENU:
            self.skyRunnerInstance.gameState = State.INGAMECREDITSMENU
            if not self.credits:
                self.credits = Credits(self.skyRunnerInstance)
            else:
                self.credits.show()
            
    def resumeGame( self ):
        if self.skyRunnerInstance.gameState == State.INGAMEMENU:
            self.skyRunnerInstance.escPressed()
            
    def endGame( self ):
        if self.skyRunnerInstance.gameState == State.INGAMEMENU:
            sys.exit()  