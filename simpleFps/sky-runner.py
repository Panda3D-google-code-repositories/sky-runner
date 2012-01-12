import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
import sys

class Game(object):

    def __init__(self):
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

        OnscreenText(text="Sky-Runner: Mirror's Edge-like Game", style=1, fg=(1,0,0,1),
                    pos=(1.3,-0.95), align=TextNode.ARight, scale = .07)
        #OnscreenText(text=__doc__, style=1, fg=(1,1,1,1),
        #            pos=(-1.3, 0.95), align=TextNode.ALeft, scale = .05)


    def initCollision(self):
        """ create the collision system """
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()


    def loadLevel(self):
        """ load the self.level 
            must have
            <Group> *something* { 
              <Collide> { Polyset keep descend } 
            in the egg file
        """
        self.level = loader.loadModel('level.egg')
        self.level.reparentTo(render)
        self.level.setTwoSided(True)


    def initPlayer(self):
        """ loads the player and creates all the controls for him"""
        self.player = Player()


class Player(object):

    MouseSensitivity = 0.2
    Speed = 30

    FORWARD = Vec3( 0, 2, 0)
    BACK    = Vec3( 0,-1, 0)
    LEFT    = Vec3(-1, 0, 0)
    RIGHT   = Vec3( 1, 0, 0)
    STOP    = Vec3( 0, 0, 0)

    walk   = STOP
    strafe = STOP

    readyToJump = False
    JumpMomentum = 0
    JumpMultiplier = 3


    def __init__(self):
        """ inits the player """
        self.loadModel()
        self.setUpCamera()
        self.createCollisions()
        self.attachControls()

        taskMgr.add( self.mouseUpdate, 'mouse-task' )
        taskMgr.add( self.moveUpdate,  'move-task'  )
        taskMgr.add( self.jumpUpdate,  'jump-task'  )


    def loadModel(self):
        """ make the nodepath for player """
        self.player = NodePath('player')
        self.player.reparentTo(render)
        self.player.setPos(0,0,2)
        self.player.setScale(.05)


    def setUpCamera(self):
        """ puts camera at the players node """
        pl =  base.cam.node().getLens()
        pl.setFov(80)
        base.cam.node().setLens(pl)
        base.camera.reparentTo(self.player)


    def createCollisions(self):
        """ create a collision solid and ray for the player """
        cn = CollisionNode('player')
        cn.addSolid(CollisionSphere(0,0,0,3))
        solid = self.player.attachNewNode(cn)
        base.cTrav.addCollider(solid,base.pusher)
        base.pusher.addCollider(solid,self.player, base.drive.node())

        # init players floor collisions
        ray = CollisionRay()
        ray.setOrigin(0,0,-.2)
        ray.setDirection(0,0,-1)
        cn = CollisionNode('playerRay')
        cn.addSolid(ray)
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        solid = self.player.attachNewNode(cn)
        self.playerGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.playerGroundHandler)


    def attachControls(self):
        """ attach key events """
        base.accept( "space" ,    self.__setattr__, [ "readyToJump", True  ] )
        base.accept( "space-up" , self.__setattr__, [ "readyToJump", False ] )
        base.accept( "w" ,    self.__setattr__, [ "walk", self.FORWARD ] )
        base.accept( "w-up" , self.__setattr__, [ "walk", self.STOP    ] )
        base.accept( "s" ,    self.__setattr__, [ "walk", self.BACK    ] )
        base.accept( "s-up" , self.__setattr__, [ "walk", self.STOP    ] )
        base.accept( "a" ,    self.__setattr__, [ "strafe", self.LEFT  ] )
        base.accept( "a-up" , self.__setattr__, [ "strafe", self.STOP  ] )
        base.accept( "d" ,    self.__setattr__, [ "strafe", self.RIGHT ] )
        base.accept( "d-up" , self.__setattr__, [ "strafe", self.STOP  ] )


    def mouseUpdate(self,task):
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if base.win.movePointer( 0, base.win.getXSize()/2, base.win.getYSize()/2 ):
            self.player.setH( self.player.getH() - ( x - base.win.getXSize() / 2 ) * self.MouseSensitivity )
            base.camera.setP( base.camera.getP() - ( y - base.win.getYSize() / 2 ) * self.MouseSensitivity )
        return task.cont


    def moveUpdate(self,task): 
        self.player.setPos( self.player, self.walk   * globalClock.getDt() * self.Speed )
        self.player.setPos( self.player, self.strafe * globalClock.getDt() * self.Speed )
        return task.cont


    def jumpUpdate(self,task):
        # get the highest Z from the down casting ray
        highestZ = -1000
        for i in range(self.playerGroundHandler.getNumEntries()):
            entry = self.playerGroundHandler.getEntry(i)
            z = entry.getSurfacePoint(render).getZ()
            if z > highestZ and entry.getIntoNode().getName() == "Cube":
                highestZ = z
        # gravity effects and jumps
        self.player.setZ( self.player.getZ() + self.JumpMomentum * self.JumpMultiplier * globalClock.getDt() )
        self.JumpMomentum -= self.JumpMultiplier * globalClock.getDt()
        if highestZ > self.player.getZ() - 0.3:
            self.JumpMomentum = 0
            self.player.setZ( highestZ + 0.3 )
            if self.readyToJump:
                self.JumpMomentum = 1
        return task.cont

Game()
run() 
