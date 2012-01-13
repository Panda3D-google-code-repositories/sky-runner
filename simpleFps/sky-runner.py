import direct.directbase.DirectStart
import sys
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

        self.curSpeedText = OnscreenText(text = "CurSpeed = 0", style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.95 ), align = TextNode.ALeft, scale = .05 )
        self.curStrafeSpeedText = OnscreenText(text = "CurStrafeSpeed = 0", style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.90 ), align = TextNode.ALeft, scale = .05 )
        self.camCurRollText = OnscreenText(text = "CamCurRoll = 0", style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.85 ), align = TextNode.ALeft, scale = .05 )

        taskMgr.add( self.messageUpdate, 'MessageTask' )


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
        self.level = loader.loadModel('level.egg')
        self.level.reparentTo(render)
        self.level.setTwoSided(True)


    def initPlayer( self ):
        """ loads the player and creates all the controls for him"""
        self.player = Player()


    def messageUpdate( self, task ):

        self.curSpeedText.destroy()
        self.curSpeedText = OnscreenText(text = "CurSpeed = " + str( self.player.CurSpeed ), style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.95 ), align = TextNode.ALeft, scale = .05 )

        self.curStrafeSpeedText.destroy()
        self.curStrafeSpeedText = OnscreenText(text = "CurStrafeSpeed = " + str( self.player.CurStrafeSpeed ), style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.90 ), align = TextNode.ALeft, scale = .05 )

        self.camCurRollText.destroy()
        self.camCurRollText = OnscreenText(text = "CamCurRoll = " + str( self.player.CameraCurRoll ), style = 1, fg = ( 1, 0, 0, 1 ),
                            pos = ( 0.65, 0.85 ), align = TextNode.ALeft, scale = .05 )

        return task.cont

Game()
run()
