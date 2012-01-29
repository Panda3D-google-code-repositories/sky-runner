import direct.directbase.DirectStart
import sys
import datetime
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

from player import Player
from GameStates import State

loadPrcFileData("", "framebuffer-multisample 1")
loadPrcFileData("", "multisamples 2")

class Game( object ):

    def __init__( self, skyRunner ):
        self.skyRunnerInstance = skyRunner
        self.initCollision()
        self.loadLevel()
        self.initPlayer()
        
        self.fVidas1 = DirectFrame(frameSize=(0.9,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/wingLetters.png",image_pos=(0.9,-0.8,0.9),image_scale=(0.1,0.1,0.1), sortOrder=(-1))
        self.fVidas1.setTransparency(TransparencyAttrib.MAlpha)
        self.fVidas2 = DirectFrame(frameSize=(0.7,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/wingLetters.png",image_pos=(0.75,-0.8,0.9),image_scale=(0.1,0.1,0.1), sortOrder=(-1))
        self.fVidas2.setTransparency(TransparencyAttrib.MAlpha)
        self.fVidas3 = DirectFrame(frameSize=(0.5,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/wingLetters.png",image_pos=(0.55,-0.8,0.9),image_scale=(0.1,0.1,0.1), sortOrder=(-1))
        self.fVidas3.setTransparency(TransparencyAttrib.MAlpha)
        
        self.vVidas = [self.fVidas1,self.fVidas2,self.fVidas3]
        
        #self.fVidas2 = DirectFrame(frameSize=(-0.5,0.5,-0.5,0.5), parent=render2d, image="hud.Sources/wingLetters.png", sortOrder=(-1))self.fVidas1 = DirectFrame(frameSize=(-0.5,0.5,-0.5,0.5), parent=render2d, image="hud.Sources/wingLetters.png", sortOrder=(-1))
        #self.fVidas3 = DirectFrame(frameSize=(-0.5,0.5,-0.5,0.5), parent=render2d, image="hud.Sources/wingLetters.png", sortOrder=(-1))self.fVidas1 = DirectFrame(frameSize=(-0.5,0.5,-0.5,0.5), parent=render2d, image="hud.Sources/wingLetters.png", sortOrder=(-1))

        self.fVidas1.show()
        self.fVidas2.show()
        self.fVidas3.show()
        # Make the mouse invisible, turn off normal mouse controls
        self.toggleMouseControls(False)
        
        self.paused = False
        self.pausedTime = datetime.timedelta(seconds=0)
        self.pausedX = 0
        self.pausedY = 0
        
        self.title = OnscreenText(text = "Sky-Runner: Mirror's Edge-like Game", style = 1, fg = ( 1, 0, 0, 1 ),
                                pos = ( 1.32, -0.98 ), align=TextNode.ARight, scale = .07 )

        self.inst1 = OnscreenText(text = "[ESC]: Quit", style = 1, fg = ( 1, 0, 0, 1 ),
                                pos = ( -1.33, 0.95 ), align = TextNode.ALeft, scale = .05 )
        self.inst2 = OnscreenText(text = "[mouse]: Move Camera", style = 1, fg = ( 1, 0, 0, 1 ),
                                pos = ( -1.33, 0.90 ), align = TextNode.ALeft, scale = .05 )
        self.inst3 = OnscreenText(text = "[W]: Move Forward", style = 1, fg = ( 1, 0, 0, 1 ),
                                pos = ( -1.33, 0.85 ), align = TextNode.ALeft, scale = .05 )
        self.inst4 = OnscreenText(text = "[S]: Move Backward", style = 1, fg = ( 1, 0, 0, 1 ),
                                pos = ( -1.33, 0.80 ), align = TextNode.ALeft, scale = .05 )
        self.inst5 = OnscreenText(text = "[A]: Strafe Left", style = 1, fg = ( 1, 0, 0, 1 ),
                                pos = ( -1.33, 0.75 ), align = TextNode.ALeft, scale = .05 )
        self.inst6 = OnscreenText(text = "[D]: Strafe Right", style = 1, fg = ( 1, 0, 0, 1 ),
                                pos = ( -1.33, 0.70 ), align = TextNode.ALeft, scale = .05 )
        self.inst7 = OnscreenText(text = "[space]: Jump", style = 1, fg = ( 1, 0, 0, 1 ),
                                pos = ( -1.33, 0.65 ), align = TextNode.ALeft, scale = .05 )
        self.inst8 = OnscreenText(text = "[R]: Roll", style = 1, fg = ( 1, 0, 0, 1 ),
                                pos = ( -1.33, 0.60 ), align = TextNode.ALeft, scale = .05 )

        self.curSpeedText = OnscreenText(text = "CurSpeed = 0", style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.95 ), align = TextNode.ALeft, scale = .05 )
        self.curStrafeSpeedText = OnscreenText(text = "CurStrafeSpeed = 0", style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.90 ), align = TextNode.ALeft, scale = .05 )
        self.fallHeightText = OnscreenText(text = "FallHeight = 0", style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.85 ), align = TextNode.ALeft, scale = .05 )

        self.currCheckPointText = OnscreenText(text = "Current CheckPoint: " + str( self.player.currentCheckPoint ), style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( .1, -0.98 ), align=TextNode.ARight, scale = .07 )
                            
        taskMgr.add( self.messageUpdate, 'MessageTask' )
        taskMgr.add( self.taskFade, 'fadeTask' )
        

        # timer
        self.clock = OnscreenText(scale = .15, mayChange = True, pos= (-0.5,0.87), fg= (0,1,0,1))
        self.startTime = datetime.datetime.today()
        self.lastTimeStop = datetime.timedelta(seconds=0)
        self.displayTime = datetime.timedelta(seconds=0)
        self.timerTask = taskMgr.add( self.timer, 'TimerTask' )
        
            
        self.solarBeam = render.attachNewNode(DirectionalLight('sun'))
        self.solarBeam.node().setColor(Vec4(0.7, 0.7, 0.7, 1))
        self.solarBeam.setHpr(0,-60,0)
        self.solarBeam.setPos(0,-450,340)
        
        self.ambientLight = render.attachNewNode(AmbientLight('ambient light'))
        self.ambientLight.node().setColor(Vec4(0.3, 0.3, 0.3, 1))
        
        self.solarBeam.node().setLens(base.cam.node().getLens())
        self.solarBeam.node().setShadowCaster(True, 4096, 4096)
        self.solarBeam.node().showFrustum()
        self.solarBeam.node().getLens().setFilmSize(4096, 4096)
        
        
        #render.setShaderAuto()
        render.setLight(self.solarBeam)
        render.setLight(self.ambientLight)
        render.setAntialias(AntialiasAttrib.MMultisample)

    def initCollision( self ):
        """ create the collision system """
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()


    def loadLevel( self ):
        """ load the self.level 
            must have
            <Group> *something* { 
              <Collide> { Polyset keep descend } 
            in the egg file
        """
        self.level = loader.loadModel('level.Sources/levelDesign-01.egg')
        self.level.reparentTo(render)
        self.level.setTwoSided(True)
        self.level.setPos(0.0,0.0,0.0)
        self.level.setAntialias(AntialiasAttrib.MMultisample)

        self.myFog = Fog("Fog Name")
        self.myFog.setColor(0.2,0.2,0.2)
        self.myFog.setExpDensity(0.0)
        self.level.setFog(self.myFog)
        
        #self.level.setShaderAuto()


    def initPlayer( self ):
        """ loads the player and creates all the controls for him"""
        self.player = Player( self )
        self.player.player.setPos(-34.0,30.0,3.0)


    def messageUpdate( self, task ):
        self.curSpeedText.destroy()
        self.curSpeedText = OnscreenText(text = "CurSpeed = " + str( self.player.CurSpeed ), style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.95 ), align = TextNode.ALeft, scale = .05 )

        self.curStrafeSpeedText.destroy()
        self.curStrafeSpeedText = OnscreenText(text = "CurStrafeSpeed = " + str( self.player.CurStrafeSpeed ), style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.90 ), align = TextNode.ALeft, scale = .05 )

        self.fallHeightText.destroy()
        self.fallHeightText = OnscreenText(text = "FallHeight = " + str( self.player.FallHeight ), style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.85 ), align = TextNode.ALeft, scale = .05 )
                            
        self.currCheckPointText.destroy()
        self.currCheckPointText = OnscreenText(text = "Current CheckPoint: " + str( self.player.currentCheckPoint ), style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( .1, -0.98 ), align=TextNode.ARight, scale = .07 )

        return task.cont
        
    def timer( self, task ): 
      nowTime = datetime.datetime.today()
      t = self.lastTimeStop + nowTime - self.startTime
      self.displayTime = t
      
      s = str(t).split(':')
      
      s2 = s[2].split('.')
      if len(s2) == 1:
       s2.append('00')
      self.clock.setText(':'.join(s[:2])+':'+s2[0]+'\''+s2[1][:1])
      
      return task.cont

    def addTasks( self ):
        taskMgr.add( self.messageUpdate, 'MessageTask' )
        self.timerTask = taskMgr.add( self.timer, 'TimerTask' )
        taskMgr.add( self.player.mouseUpdate, 'MouseTask' )
        taskMgr.add( self.player.moveUpdate,  'MoveTask'  )
        taskMgr.add( self.player.jumpUpdate,  'JumpTask'  )
        
    def removeTasks( self ):
        taskMgr.remove( 'MessageTask' )
        taskMgr.remove( 'TimerTask' )
        taskMgr.remove( 'MouseTask' )
        taskMgr.remove( 'MoveTask'  )
        taskMgr.remove( 'JumpTask'  )
        
    def pauseGame( self ):
        
        if self.paused == False:
            self.removeTasks()
            self.pausedTime = self.displayTime
            
            md = base.win.getPointer(0)
            self.pausedX = md.getX()
            self.pausedY = md.getY()

            self.paused = True
        else:
            self.addTasks()
            self.startTime = datetime.datetime.today()
            self.lastTimeStop = self.pausedTime
            md = base.win.getPointer(0)
            base.win.movePointer(0, self.pausedX , self.pausedY)
        
            self.paused = False
        
    def toggleMouseControls(self, b):
        props = WindowProperties()
        if b == True:
            base.enableMouse()
            props.setCursorHidden( False )
        else:
            base.disableMouse()
            props.setCursorHidden( True )
            
        base.win.requestProperties( props )
        
    def clearScreenTexts( self ):
        self.title.destroy()
        self.inst1.destroy()
        self.inst2.destroy()
        self.inst3.destroy()
        self.inst4.destroy()
        self.inst5.destroy()
        self.inst6.destroy()
        self.inst7.destroy()
        self.inst8.destroy()
        self.curSpeedText.destroy()
        self.curStrafeSpeedText.destroy()
        self.fallHeightText.destroy()
        self.currCheckPointText.destroy()
        self.clock.destroy()
        
    def taskFade( self, task ):
        if self.paused == True:
            if self.myFog.getExpDensity() < 0.4:

                self.myFog.setExpDensity(self.myFog.getExpDensity()+0.001) 
        else:
            if self.myFog.getExpDensity() >0.000001:
                tmp = self.myFog.getExpDensity()-0.01
                if tmp < 0:
                    tmp = 0
                self.myFog.setExpDensity(tmp) 
            
        return task.cont
        
#Game()
#run()
