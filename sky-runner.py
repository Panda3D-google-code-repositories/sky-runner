import direct.directbase.DirectStart
import sys
import datetime
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from player import Player

class Game( object ):

    def __init__( self ):
        """ create a FPS type game """
        self.initCollision()
        self.loadLevel()
        self.initPlayer()

        base.accept( "escape" , sys.exit)

        # Make the mouse invisible, turn off normal mouse controls
        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden( True )
        base.win.requestProperties( props )

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
        self.inst7 = OnscreenText(text = "[R]: Roll", style = 1, fg = ( 1, 0, 0, 1 ),
                                pos = ( -1.33, 0.60 ), align = TextNode.ALeft, scale = .05 )

        self.curSpeedText = OnscreenText(text = "CurSpeed = 0", style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.95 ), align = TextNode.ALeft, scale = .05 )
        self.curStrafeSpeedText = OnscreenText(text = "CurStrafeSpeed = 0", style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.90 ), align = TextNode.ALeft, scale = .05 )
        self.fallHeightText = OnscreenText(text = "FallHeight = 0", style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.85 ), align = TextNode.ALeft, scale = .05 )

        taskMgr.add( self.messageUpdate, 'MessageTask' )

        # timer
        self.clock = OnscreenText(scale = .15, mayChange = True, pos= (-0.5,0.87), fg= (0,1,0,1))
        self.startTime = datetime.datetime.today()
        self.timerTask = taskMgr.add( self.timer, 'Timer' )
        
            
        self.solarBeam = render.attachNewNode(DirectionalLight('sun'))
        self.solarBeam.node().setColor(Vec4(0.7, 0.7, 0.7, 1))
        self.solarBeam.setHpr(0,-60,0)
        self.solarBeam.setPos(0,-450,340)
        
        self.ambientLight = render.attachNewNode(AmbientLight('ambient light'))
        self.ambientLight.node().setColor(Vec4(0.3, 0.3, 0.3, 1))
        
        self.solarBeam.node().setLens(base.cam.node().getLens())
        self.solarBeam.node().setShadowCaster(True, 4096, 4096)
        #self.solarBeam.node().showFrustum()
        self.solarBeam.node().getLens().setFilmSize(4096, 4096)
        
        
        render.setShaderAuto()
        render.setLight(self.solarBeam)
        render.setLight(self.ambientLight)
        render.setAntialias(AntialiasAttrib.MAuto)

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
        self.level.setShaderAuto()


    def initPlayer( self ):
        """ loads the player and creates all the controls for him"""
        self.player = Player()
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

        return task.cont
        
    def timer( self, task ): 
      nowTime = datetime.datetime.today()
      t = nowTime - self.startTime
      s = str(t).split(':')
      
      s2 = s[2].split('.')
      if len(s2) == 1:
       s2.append('00')
      self.clock.setText(':'.join(s[:2])+':'+s2[0]+'\''+s2[1][:1])
      
      return task.cont

Game()
run()
