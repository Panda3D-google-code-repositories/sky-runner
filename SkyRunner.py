import sys

from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage

from InGameMenu import InGameMenu
from Credits import Credits
from Game import Game
from GameStates import State
from SoundManager import SoundManager

import direct.directbase.DirectStart
    
class SkyRunner(DirectObject.DirectObject):
    def __init__(self,cond=1):
        self.gameState = State.MAINMENU
        
        base.accept( "escape" , self.escPressed )
        
        self.soundManager = SoundManager()
        self.draw() 
        self.show()
        self.credits = None    
        self.game = None
        self.inGameMenu = None
        

    def draw( self ): 
        self.frame = DirectFrame(frameSize=(-0.5, 0.5, -0.5, 0.5), frameColor=(0.8,0.8,0.8,0), pos=(0,0,0))
        self.frame2 = DirectFrame(frameSize=(-0.5,0.5,-0.5,0.5), parent=render2d, image="hud.Sources/TitleScreen.jpg", sortOrder=(-1))
                
        #self.startButton = DirectButton(parent=self.frame, text="Start Game", command=self.doStartGame, pos=(1,0,-0.5), text_scale=0.08, text_fg=(1,1,1,1), text_align=TextNode.ACenter, borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06), frameColor=(0.8,0.8,0.8,0)) 
        mapsStart = loader.loadModel('hud.Sources/mainMenu/buttons_start_maps.egg')        
        self.startButton = DirectButton(parent=self.frame,pos=(1,0,-0.5),image = (mapsStart.find('**/startready'),
                         mapsStart.find('**/startclicked'),
                         mapsStart.find('**/startrollover'),
                         mapsStart.find('**/startdisable')),command=self.doStartGame, scale=0.2,
                         borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06),  
                         frameColor=(0.8,0.8,0.8,0), rolloverSound=self.soundManager.over,clickSound=self.soundManager.click)
        
        #self.creditsButton = DirectButton(parent=self.frame, text="Credits", command=self.showCredits, pos=(1.075,0,-0.6), text_scale=0.08, text_fg=(1,1,1,1), text_align=TextNode.ACenter, borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06), frameColor=(0.8,0.8,0.8,0))
        mapsCredits = loader.loadModel('hud.Sources/mainMenu/buttons_credits_maps.egg')
        self.creditsButton = DirectButton(parent=self.frame,pos=(1.075,0,-0.6),image = (mapsCredits.find('**/creditsready'),
                         mapsCredits.find('**/creditsclicked'),
                         mapsCredits.find('**/creditsrollover'),
                         mapsCredits.find('**/creditsdisable')),command=self.showCredits, scale=0.2,
                         borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06),  
                         frameColor=(0.8,0.8,0.8,0),rolloverSound=self.soundManager.over,clickSound=self.soundManager.click)
        

        #self.quitButton = DirectButton(parent=self.frame, text="Quit", command=self.endGame, pos=(1.13,0,-0.7), text_scale=0.08, text_fg=(1,1,1,1), text_align=TextNode.ACenter, borderWidth=(0.005,0.005), frameSize=(-0.25, 0.25, -0.03, 0.06), frameColor=(0.8,0.8,0.8,0))
        mapsQuit = loader.loadModel('hud.Sources/mainMenu/buttons_quit_maps.egg')
        self.quitButton = DirectButton(parent=self.frame,pos=(1.13,0,-0.7),image = (mapsQuit.find('**/quitready'),
                         mapsQuit.find('**/quitclicked'),
                         mapsQuit.find('**/quitrollover'),
                         mapsQuit.find('**/quitdisable')),command=self.endGame, scale=0.2,borderWidth=(0.005,0.005),
                         frameSize=(-0.25, 0.25, -0.03, 0.06),  frameColor=(0.8,0.8,0.8,0),rolloverSound=self.soundManager.over,clickSound=self.soundManager.click)
                         
    def show( self ):
        self.gameState = State.MAINMENU
        self.frame.show()
        self.frame2.show()
        
    def hide(self):
        self.frame.destroy()
        self.frame2.destroy()     
        
    def doStartGame(self):
        if self.gameState == State.MAINMENU:
            self.gameState = State.INGAME
            self.hide()
            if not self.game:
                self.game = Game(self)     
    def showCredits(self):
        if self.gameState == State.MAINMENU:
            self.gameState = State.CREDITSMENU
        
            if not self.credits:
                self.credits = Credits(self)
            else:
                self.credits.show()
            
    def showInGameMenu(self):
        self.gameState = State.INGAMEMENU
        
        if not self.inGameMenu:
            self.inGameMenu = InGameMenu(self)
        else:
            self.inGameMenu.show()
        
    def escPressed( self ):
        if self.gameState == State.MAINMENU:
            sys.exit()
        
        if self.gameState == State.CREDITSMENU:
            self.credits.hide()
            self.gameState = State.MAINMENU
            return
        
        if self.gameState == State.INGAME:
            self.game.pauseGame()
            self.game.toggleMouseControls(True)
            #self.game.myFog.setExpDensity(0.8)
            self.showInGameMenu()
            return
        
        if self.gameState == State.INGAMEMENU:
            self.game.pauseGame()
            #self.game.myFog.setExpDensity(0.0)
            self.game.toggleMouseControls(False)
            self.inGameMenu.hide()
            self.gameState = State.INGAME
            return
        
        if self.gameState == State.INGAMECREDITSMENU:
            self.inGameMenu.credits.hide()
            self.gameState = State.INGAMEMENU
    
    def endGame( self ):
        if self.gameState == State.MAINMENU:
            sys.exit()

SkyRunner()
run()