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

        OnscreenText(text = "Sky-Runner: Mirror's Edge-like Game", style = 1, fg = ( 1, 0, 0, 1 ),
                    pos = ( 1.32, -0.98 ), align=TextNode.ARight, scale = .07 )
        OnscreenText(text = "[ESC]: Quit", style = 1, fg = ( 1, 0, 0, 1 ),
                    pos = ( -1.33, 0.95 ), align = TextNode.ALeft, scale = .05 )
        OnscreenText(text = "[mouse]: Move Camera", style = 1, fg = ( 1, 0, 0, 1 ),
                    pos = ( -1.33, 0.90 ), align = TextNode.ALeft, scale = .05 )
        OnscreenText(text = "[W]: Move Forward", style = 1, fg = ( 1, 0, 0, 1 ),
                    pos = ( -1.33, 0.85 ), align = TextNode.ALeft, scale = .05 )
        OnscreenText(text = "[S]: Move Backward", style = 1, fg = ( 1, 0, 0, 1 ),
                    pos = ( -1.33, 0.80 ), align = TextNode.ALeft, scale = .05 )
        OnscreenText(text = "[A]: Strafe Left", style = 1, fg = ( 1, 0, 0, 1 ),
                    pos = ( -1.33, 0.75 ), align = TextNode.ALeft, scale = .05 )
        OnscreenText(text = "[D]: Strafe Right", style = 1, fg = ( 1, 0, 0, 1 ),
                    pos = ( -1.33, 0.70 ), align = TextNode.ALeft, scale = .05 )
        OnscreenText(text = "[space]: Jump", style = 1, fg = ( 1, 0, 0, 1 ),
                    pos = ( -1.33, 0.65 ), align = TextNode.ALeft, scale = .05 )


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


Game()
run()
