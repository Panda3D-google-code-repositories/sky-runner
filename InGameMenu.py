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
        
        mapsMainMenu = loader.loadModel('hud.Sources/mainMenu/buttons_mainmenu_maps.egg')        
        self.startButton = DirectButton(parent=self.frame,pos=(0,0,0.1),image = (mapsMainMenu.find('**/mainmenuready'),
                         mapsMainMenu.find('**/mainmenuclicked'),
                         mapsMainMenu.find('**/mainmenurollover'),
                         mapsMainMenu.find('**/mainmenudisable')),command=self.showMainMenu, scale=0.2,borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06),  frameColor=(0.8,0.8,0.8,0))

        mapsCredits = loader.loadModel('hud.Sources/mainMenu/buttons_credits_maps.egg')
        self.b = DirectButton(parent=self.frame,pos=(0,0,0),image = (mapsCredits.find('**/creditsready'),
                         mapsCredits.find('**/creditsclicked'),
                         mapsCredits.find('**/creditsrollover'),
                         mapsCredits.find('**/creditsdisable')),command=self.showCredits, scale=0.2,borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06),  frameColor=(0.8,0.8,0.8,0))
        
        mapsResume = loader.loadModel('hud.Sources/mainMenu/buttons_resume_maps.egg')
        self.b = DirectButton(parent=self.frame,pos=(0,0,-0.1),image = (mapsResume.find('**/resumeready'),
                         mapsResume.find('**/resumeclicked'),
                         mapsResume.find('**/resumerollover'),
                         mapsResume.find('**/resumedisable')),command=self.resumeGame, scale=0.2,borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06),  frameColor=(0.8,0.8,0.8,0))

        mapsQuit = loader.loadModel('hud.Sources/mainMenu/buttons_quit_maps.egg')
        self.quitButton = DirectButton(parent=self.frame,pos=(0,0,-0.2),image = (mapsQuit.find('**/quitready'),
                         mapsQuit.find('**/quitclicked'),
                         mapsQuit.find('**/quitrollover'),
                         mapsQuit.find('**/quitdisable')),command=self.endGame, scale=0.2,borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06),  frameColor=(0.8,0.8,0.8,0))

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