import sys

from pandac.PandaModules import *

from direct.showbase import DirectObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage

from pandac.PandaModules import AntialiasAttrib

from Credits import Credits
from GameStates import State

#loadPrcFileData("", "framebuffer-multisample 1")
#loadPrcFileData("", "multisamples 2")


class InGameMenu(DirectObject.DirectObject):
    def __init__( self, skyRunner ):
        self.skyRunnerInstance = skyRunner
        self.frame = DirectFrame(frameSize=(-0.3, 0.3, -0.6, 0.4))
        self.frame['frameColor']=(0.8,0.8,0.8,0)
        self.frame['image'] = "hud.Sources/menuInGame.png"
        self.frame['image_scale'] = 0.7
        self.frame['pos'] = (-.3,0,-.6)
        self.frame.setTransparency(TransparencyAttrib.MAlpha)
        #self.wingsL = OnscreenImage(parent=self.frame,image = "hud.Sources/wingLettersL.png",pos=(-0.3, 0.3, 0.5) , scale = (0.2,0.2,0.2))
        #self.wingsL.setTransparency(TransparencyAttrib.MAlpha)
        #self.wingsL.show()
        #self.wingsR = OnscreenImage(parent=self.frame,image = "hud.Sources/wingLetters.png",pos=(0.3, 0.3, 0.5) , scale = (0.2,0.2,0.2))
        #self.wingsR.setTransparency(TransparencyAttrib.MAlpha)
        #self.wingsR.show()

        #self.headline = DirectLabel(parent=self.frame, text="Sky Runner", scale=0.085, frameColor=(0,0,0,0), pos=(0,0,0.3))
        
        mapsMainMenu = loader.loadModel('hud.Sources/mainMenu/buttons_mainmenu_maps.egg')   
#        mapsMainMenu.setAntialias(AntialiasAttrib.MMultisample)
        self.startButton = DirectButton(parent=self.frame,pos=(0,0,0),image = (mapsMainMenu.find('**/mainmenuready'),
                         mapsMainMenu.find('**/mainmenuclicked'),
                         mapsMainMenu.find('**/mainmenurollover'),
                         mapsMainMenu.find('**/mainmenudisable')),command=self.showMainMenu, scale=0.2,
                         borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06),  
                         frameColor=(0.8,0.8,0.8,0),rolloverSound=self.skyRunnerInstance.soundManager.over,clickSound=self.skyRunnerInstance.soundManager.click)

        mapsCredits = loader.loadModel('hud.Sources/mainMenu/buttons_credits_maps.egg')
        self.creditsButton = DirectButton(parent=self.frame,pos=(0,0,-0.15),image = (mapsCredits.find('**/creditsready'),
                         mapsCredits.find('**/creditsclicked'),
                         mapsCredits.find('**/creditsrollover'),
                         mapsCredits.find('**/creditsdisable')),command=self.showCredits, scale=0.2,
                         borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06),  
                         frameColor=(0.8,0.8,0.8,0),rolloverSound=self.skyRunnerInstance.soundManager.over,clickSound=self.skyRunnerInstance.soundManager.click)
        
        mapsResume = loader.loadModel('hud.Sources/mainMenu/buttons_resume_maps.egg')
        self.resumeButton = DirectButton(parent=self.frame,pos=(0,0,-0.3),image = (mapsResume.find('**/resumeready'),
                         mapsResume.find('**/resumeclicked'),
                         mapsResume.find('**/resumerollover'),
                         mapsResume.find('**/resumedisable')),command=self.resumeGame, scale=0.2,
                         borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06),  
                         frameColor=(0.8,0.8,0.8,0),rolloverSound=self.skyRunnerInstance.soundManager.over,clickSound=self.skyRunnerInstance.soundManager.click)

        mapsQuit = loader.loadModel('hud.Sources/mainMenu/buttons_quit_maps.egg')
        self.quitButton = DirectButton(parent=self.frame,pos=(0,0,-0.45),image = (mapsQuit.find('**/quitready'),
                         mapsQuit.find('**/quitclicked'),
                         mapsQuit.find('**/quitrollover'),
                         mapsQuit.find('**/quitdisable')),command=self.endGame, scale=0.2,borderWidth=(0.005,0.005),
                         frameSize=(-0.25, 0.25, -0.03, 0.06),  frameColor=(0.8,0.8,0.8,0),
                         rolloverSound=self.skyRunnerInstance.soundManager.over,clickSound=self.skyRunnerInstance.soundManager.click)

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