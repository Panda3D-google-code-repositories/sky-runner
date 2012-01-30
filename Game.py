import direct.directbase.DirectStart
import sys
import datetime
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from pandac.PandaModules import TransparencyAttrib
from pandac.PandaModules import AntialiasAttrib

from player import Player
from GameStates import State

#loadPrcFileData("", "framebuffer-multisample 1")
#loadPrcFileData("", "multisamples 2")

class Game( object ):

    def __init__( self, skyRunner ):
        self.skyRunnerInstance = skyRunner
        self.initCollision()
        self.loadLevel()
        self.initPlayer()
        self.initSounds()

        
        self.frameWin = DirectFrame(frameSize=(-0.3, 0.3, -0.6, 0.4))
        self.frameWin['frameColor']=(0.8,0.8,0.8,0)
        self.frameWin['pos'] = (-.3,0,-.6)
        self.frameWin.setTransparency(TransparencyAttrib.MAlpha)
        self.frameWin.show()
        
        self.timeFont = loader.loadFont('hud.Sources/fonts/moderna.ttf')
        self.textTimer = TextNode('Time')    
        self.textTimer.setFont(self.timeFont)   
        self.textTimer.setShadow(0.05, 0.05)
        self.textTimer.setShadowColor(0, 0, 0, 1) 
        self.textTimerNodePath = aspect2d.attachNewNode(self.textTimer) 
        self.textTimerNodePath.setScale(0.05) 
        self.textTimerNodePath.reparentTo(base.a2dTopRight) 
        self.textTimerNodePath.setPos(-0.5, 0, -0.17) 

        self.textRecord = TextNode('Record')    
        self.textRecord.setFont(self.timeFont)   
        self.textRecord.setShadow(0.05, 0.05)
        self.textRecord.setShadowColor(0, 0, 0, 1) 
        self.textRecordNodePath = aspect2d.attachNewNode(self.textRecord) 
        self.textRecordNodePath.setScale(0.035) 
        self.textRecordNodePath.reparentTo(base.a2dTopRight) 
        self.textRecordNodePath.setPos(-0.415, 0, -0.21) 
                        
        
        self.lifes = NodePath('Lifes')
        self.lifes.reparentTo(base.a2dTopRight)
        
        self.fVidas1On = OnscreenImage(parent=self.lifes,image = "hud.Sources/lifeOn.png",pos=(-0.1, 0, -0.1) , scale = (0.1,0.02,0.02))#DirectFrame(frameSize=(0.9,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/lifeOn.png",image_pos=(0.9,-0.8,0.9),scale = (0.2,0.04,0.04), sortOrder=(-1))
        self.fVidas1Off = OnscreenImage(parent=self.lifes,image = "hud.Sources/lifeOff.png",pos=(-0.1, 0, -0.1), scale = (0.1,0.02,0.02))#DirectFrame(frameSize=(0.9,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/lifeOff.png",image_pos=(0.9,-0.8,0.9),scale = (0.2,0.04,0.04), sortOrder=(-1))
        self.fVidas1On.setTransparency(TransparencyAttrib.MAlpha)
#        self.fVidas1On.setAntialias(AntialiasAttrib.MMultisample)
        self.fVidas1Off.setTransparency(TransparencyAttrib.MAlpha)
#        self.fVidas1Off.setAntialias(AntialiasAttrib.MMultisample)
        
        self.fVidas2On = OnscreenImage(parent=self.lifes,image = "hud.Sources/lifeOn.png",pos=(-0.3, 0, -0.1), scale = (0.1,0.02,0.02))#DirectFrame(frameSize=(0.9,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/lifeOn.png",image_pos=(0.7,-0.8,0.9),scale = (0.2,0.04,0.04), sortOrder=(-1))
        self.fVidas2Off = OnscreenImage(parent=self.lifes,image = "hud.Sources/lifeOff.png",pos=(-0.3, 0, -0.1), scale = (0.1,0.02,0.02))#DirectFrame(frameSize=(0.9,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/lifeOff.png",image_pos=(0.7,-0.8,0.9),scale = (0.2,0.04,0.04), sortOrder=(-1))
        self.fVidas2On.setTransparency(TransparencyAttrib.MAlpha)
#        self.fVidas2On.setAntialias(AntialiasAttrib.MMultisample)
        self.fVidas2Off.setTransparency(TransparencyAttrib.MAlpha)
#        self.fVidas2Off.setAntialias(AntialiasAttrib.MMultisample)
        
        self.fVidas3On = OnscreenImage(parent=self.lifes,image = "hud.Sources/lifeOn.png",pos=(-0.5,0,-0.1), scale = (0.1,0.02,0.02))#DirectFrame(frameSize=(0.9,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/lifeOn.png",image_pos=(0.5,-0.8,0.9),scale = (0.2,0.04,0.04), sortOrder=(-1))
        self.fVidas3Off = OnscreenImage(parent=self.lifes,image = "hud.Sources/lifeOff.png",pos=(-0.5,0,-0.1), scale = (0.1,0.02,0.02))#DirectFrame(frameSize=(0.9,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/lifeOff.png",image_pos=(0.5,-0.8,0.9),scale = (0.2,0.04,0.04), sortOrder=(-1))
        self.fVidas3On.setTransparency(TransparencyAttrib.MAlpha)
#        self.fVidas3On.setAntialias(AntialiasAttrib.MMultisample)
        self.fVidas3Off.setTransparency(TransparencyAttrib.MAlpha)
#        self.fVidas3Off.setAntialias(AntialiasAttrib.MMultisample)
        
        self.vVidasOn = [self.fVidas1On,self.fVidas2On,self.fVidas3On]
        self.vVidasOff = [self.fVidas1Off,self.fVidas2Off,self.fVidas3Off]
        
        #self.fVidas2 = DirectFrame(frameSize=(-0.5,0.5,-0.5,0.5), parent=render2d, image="hud.Sources/wingLetters.png", sortOrder=(-1))self.fVidas1 = DirectFrame(frameSize=(-0.5,0.5,-0.5,0.5), parent=render2d, image="hud.Sources/wingLetters.png", sortOrder=(-1))
        #self.fVidas3 = DirectFrame(frameSize=(-0.5,0.5,-0.5,0.5), parent=render2d, image="hud.Sources/wingLetters.png", sortOrder=(-1))self.fVidas1 = DirectFrame(frameSize=(-0.5,0.5,-0.5,0.5), parent=render2d, image="hud.Sources/wingLetters.png", sortOrder=(-1))


        self.initHud()


        self.loadRecord()
        # Make the mouse invisible, turn off normal mouse controls
        self.toggleMouseControls(False)
        
        self.paused = False
        self.pausedTime = datetime.timedelta(seconds=0)
        self.pausedX = 0
        self.pausedY = 0
                            
        taskMgr.add( self.messageUpdate, 'MessageTask' )
        taskMgr.add( self.taskFade, 'fadeTask' )
        self.timerTask = taskMgr.add( self.timer, 'TimerTask' )
        
        self.startTime = datetime.datetime.today()
        self.lastTimeStop = datetime.timedelta(seconds=0)
        self.displayTime = datetime.timedelta(seconds=0)
            
        self.solarBeam = render.attachNewNode(DirectionalLight('sun'))#(Spotlight('sun'))
        self.solarBeam.node().setColor(Vec4(0.7, 0.7, 0.7, 1))
        self.solarBeam.setHpr(0,-90,0)
        self.solarBeam.setPos(-15,-10,80)
        
        self.ambientLight = render.attachNewNode(AmbientLight('ambient light'))
        self.ambientLight.node().setColor(Vec4(0.3, 0.3, 0.3, 1))
        
#        self.solarBeam.node().getLens().setFov(60.0)
#        self.solarBeam.node().setShadowCaster(True, 4096, 4096)
#        self.solarBeam.node().showFrustum()
#        self.solarBeam.node().getLens().setFilmSize(4096, 4096)
#        self.solarBeam.node().getLens().setNearFar(30, 1000)
        
        render.setLight(self.solarBeam)
        render.setLight(self.ambientLight)
        render.setAntialias(AntialiasAttrib.MMultisample)
        
        #render.setShaderAuto()

    def initSounds( self ):
        self.skyRunnerInstance.soundManager.soundWalking.play()
        self.skyRunnerInstance.soundManager.soundAmbient.play()
        
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
        self.level = loader.loadModel('level.Sources/levelDesignSky-01.egg')
        self.level.reparentTo(render)
        self.level.setTwoSided(True)
        self.level.setPos(0.0,0.0,0.0)
        self.level.setAntialias(AntialiasAttrib.MMultisample)
        
        self.SkyDome = loader.loadModel('level.Sources/Sky.egg')
        self.SkyDome.reparentTo(render)
        self.SkyDome.setTwoSided(True)
        self.SkyDome.setPos(0.0,0.0,0.0)
        self.SkyDome.setAntialias(AntialiasAttrib.MMultisample)
        self.SkyDome.setLightOff()
        

        self.myFog = Fog("Fog Name")
        self.myFog.setColor(0.2,0.2,0.2)
        self.myFog.setExpDensity(0.0)
        self.level.setFog(self.myFog)
        
        #self.level.setShaderAuto()


    def initPlayer( self ):
        """ loads the player and creates all the controls for him"""
        self.player = Player( self )
        self.player.player.setPos(-34.0,30.0,3.0)
        #self.player.player.setPos(32.0,-31.0,10.0)

    def initHud( self ):
        self.frameWin = DirectFrame(frameSize=(-0.3, 0.3, -0.6, 0.4))
        self.frameWin['frameColor']=(0.8,0.8,0.8,0)
        self.frameWin['pos'] = (-.3,0,-.6)
        self.frameWin.setTransparency(TransparencyAttrib.MAlpha)
        self.frameWin.show()
    
        self.timeFont = loader.loadFont('hud.Sources/fonts/moderna.ttf')
        self.textTimer = TextNode('Time')    
        self.textTimer.setFont(self.timeFont)   
        self.textTimer.setShadow(0.05, 0.05)
        self.textTimer.setShadowColor(0, 0, 0, 1) 
        self.textTimerNodePath = aspect2d.attachNewNode(self.textTimer) 
        self.textTimerNodePath.setScale(0.05) 
        self.textTimerNodePath.reparentTo(base.a2dTopRight) 
        self.textTimerNodePath.setPos(-0.5, 0, -0.17) 
        

        self.textRecord = TextNode('Record')    
        self.textRecord.setFont(self.timeFont)   
        self.textRecord.setShadow(0.05, 0.05)
        self.textRecord.setShadowColor(0, 0, 0, 1) 
        self.textRecordNodePath = aspect2d.attachNewNode(self.textRecord) 
        self.textRecordNodePath.setScale(0.035) 
        self.textRecordNodePath.reparentTo(base.a2dTopRight) 
        self.textRecordNodePath.setPos(-0.415, 0, -0.21) 
        
        
        self.lifes = NodePath('Lifes')
        self.lifes.reparentTo(base.a2dTopRight)
        
        self.fVidas1On = OnscreenImage(parent=self.lifes,image = "hud.Sources/lifeOn.png",pos=(-0.1, 0, -0.1) , scale = (0.1,0.02,0.02))#DirectFrame(frameSize=(0.9,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/lifeOn.png",image_pos=(0.9,-0.8,0.9),scale = (0.2,0.04,0.04), sortOrder=(-1))
        self.fVidas1Off = OnscreenImage(parent=self.lifes,image = "hud.Sources/lifeOff.png",pos=(-0.1, 0, -0.1), scale = (0.1,0.02,0.02))#DirectFrame(frameSize=(0.9,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/lifeOff.png",image_pos=(0.9,-0.8,0.9),scale = (0.2,0.04,0.04), sortOrder=(-1))
        self.fVidas1On.setTransparency(TransparencyAttrib.MAlpha)
        self.fVidas1Off.setTransparency(TransparencyAttrib.MAlpha)
        
        self.fVidas2On = OnscreenImage(parent=self.lifes,image = "hud.Sources/lifeOn.png",pos=(-0.3, 0, -0.1), scale = (0.1,0.02,0.02))#DirectFrame(frameSize=(0.9,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/lifeOn.png",image_pos=(0.7,-0.8,0.9),scale = (0.2,0.04,0.04), sortOrder=(-1))
        self.fVidas2Off = OnscreenImage(parent=self.lifes,image = "hud.Sources/lifeOff.png",pos=(-0.3, 0, -0.1), scale = (0.1,0.02,0.02))#DirectFrame(frameSize=(0.9,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/lifeOff.png",image_pos=(0.7,-0.8,0.9),scale = (0.2,0.04,0.04), sortOrder=(-1))
        self.fVidas2On.setTransparency(TransparencyAttrib.MAlpha)
        self.fVidas2Off.setTransparency(TransparencyAttrib.MAlpha)
        
        self.fVidas3On = OnscreenImage(parent=self.lifes,image = "hud.Sources/lifeOn.png",pos=(-0.5,0,-0.1), scale = (0.1,0.02,0.02))#DirectFrame(frameSize=(0.9,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/lifeOn.png",image_pos=(0.5,-0.8,0.9),scale = (0.2,0.04,0.04), sortOrder=(-1))
        self.fVidas3Off = OnscreenImage(parent=self.lifes,image = "hud.Sources/lifeOff.png",pos=(-0.5,0,-0.1), scale = (0.1,0.02,0.02))#DirectFrame(frameSize=(0.9,1,0.9,0.8), parent=render2d, frameColor=(0.8,0.8,0.8,.0),image="hud.Sources/lifeOff.png",image_pos=(0.5,-0.8,0.9),scale = (0.2,0.04,0.04), sortOrder=(-1))
        self.fVidas3On.setTransparency(TransparencyAttrib.MAlpha)
        self.fVidas3Off.setTransparency(TransparencyAttrib.MAlpha)
        
        self.vVidasOn = [self.fVidas1On,self.fVidas2On,self.fVidas3On]
        self.vVidasOff = [self.fVidas1Off,self.fVidas2Off,self.fVidas3Off]

        self.fVidas1On.show()
        self.fVidas2On.show()
        self.fVidas3On.show()
        self.fVidas1Off.hide()
        self.fVidas2Off.hide()
        self.fVidas3Off.hide()
        
        self.currCheckPointText = TextNode('Time')    
        self.currCheckPointText.setFont(self.timeFont)   
        self.currCheckPointText.setShadow(0.05, 0.05)
        self.currCheckPointText.setShadowColor(0, 0, 0, 1) 
        self.currCheckPointTextNodePath = aspect2d.attachNewNode(self.currCheckPointText) 
        self.currCheckPointTextNodePath.setScale(0.05) 
        self.currCheckPointTextNodePath.reparentTo(base.a2dBottomLeft) 
        self.currCheckPointTextNodePath.setPos(0.1, 0, 0.1) 
        self.currCheckPointText.setText("Current CheckPoint: " + str( self.player.currentCheckPoint ))

    def messageUpdate( self, task ):
        self.currCheckPointText.setText("Current CheckPoint: " + str( self.player.currentCheckPoint ))
        #print "Position" , self.player.player.getPos() 
        return task.cont
        
    def timer( self, task ): 
        nowTime = datetime.datetime.today()
        t = self.lastTimeStop + nowTime - self.startTime
        self.displayTime = t
      
        s = str(t).split(':')
      
        s2 = s[2].split('.')
        if len(s2) == 1:
            s2.append('00')
        self.textTimer.setText(':'.join(s[:2])+':'+s2[0]+':'+s2[1][:2])
        #self.textRecord.setText(':'.join(s[:2])+':'+s2[0]+':'+s2[1][:2])
      
        return task.cont

    def addTasks( self ):
        taskMgr.add( self.messageUpdate, 'MessageTask' )
        self.timerTask = taskMgr.add( self.timer, 'TimerTask' )
        taskMgr.add( self.player.mouseUpdate, 'MouseTask' )
        taskMgr.add( self.player.moveUpdate,  'MoveTask'  )
        taskMgr.add( self.player.jumpUpdate,  'JumpTask'  )
        taskMgr.add( self.player.fallingUpdate,  'FallingTask'  )
        
    def removeTasks( self ):
        taskMgr.remove( 'MessageTask' )
        taskMgr.remove( 'TimerTask' )
        taskMgr.remove( 'MouseTask' )
        taskMgr.remove( 'MoveTask'  )
        taskMgr.remove( 'JumpTask'  )
        taskMgr.remove( 'FallingTask'  )
        
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
        self.currCheckPointText.removeNode()
        self.textTimer.removeNode()
        self.textRecord.removeNode()
        
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
    
    def loadRecord( self ):
        hour = 10
        min = 10
        seg = 10
        mic = 10
        
        f = open( 'rec.data', 'r' )
        sTmp = f.readline()
        if not sTmp == '':
            hour = sTmp
            min = f.readline()
            seg = f.readline()
            mic = f.readline()
        
        f.close()
        
        str = hour+":"+min+":"+seg+":"+mic
        str = str.replace('\n','')
        self.textRecord.setText(str)
    
    def checkForRecord( self ):
        currTime = self.displayTime
        bestTime = currTime
        
        hour = 10
        min = 10
        seg = 10
        mic = 10
        
        f = open( 'rec.data', 'r' )
        sTmp = f.readline()
        if not sTmp == '':
            hour = int(sTmp)
            min = int(f.readline())
            seg = int(f.readline())
            mic = int(f.readline())
                
        f.close()
        
        if not hour == '':
            bestTime = datetime.timedelta(hours=hour,minutes=min,seconds=seg,milliseconds=mic)
            
        f = open( 'rec.data', 'w' )
        
        if currTime < bestTime:
            bestTime = currTime
        
        p = str(bestTime).split(':')
        
        f.write(str(p[0])+'\n')
        f.write(str(p[1])+'\n')
        s2 = p[2].split('.')
        if len(s2) == 1:
            s2.append('00')
            
        tmp = int(s2[1])
        tmp = tmp / 1000
        
        f.write(str(p[2].split('.')[0])+'\n')
        f.write(str(tmp)+'\n')
        f.close()
        
