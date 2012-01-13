from pandac.PandaModules import *

class Player(object):

    KeyMap = { "w":0, "a":0, "s":0, "d":0, "space":0 }

    MouseSensitivity = 0.2 # Higher value means faster mouse movement
    Speed = 30

    FORWARD  = Vec3( 0, 2, 0)
    BACKWARD = Vec3( 0,-1, 0)
    LEFT     = Vec3(-1, 0, 0)
    RIGHT    = Vec3( 1, 0, 0)
    STOP     = Vec3( 0, 0, 0)

    Walk   = STOP
    Strafe = STOP

    Jumping         = False
    CurJumpMomentum = 0
    MaxJumpMomentum = 3 # Higher value results in higher jumps
    JumpMultiplier  = 7 # Higher value will cause player to rise and fall faster

    CameraFOV     = 80
    CameraCurRoll = 0
    CameraMaxRoll = 0.016 # Higher value results in wider rolls
    CameraRollDt  = 0.15  # Higher value results in faster rolls
    PitchMax      = 60    # Camera can't look up or down past this value


    def __init__(self):
        """ inits the player """
        self.loadModel()
        self.setUpCamera()
        self.createCollisions()
        self.attachControls()

        taskMgr.add( self.mouseUpdate, 'MouseTask' )
        taskMgr.add( self.moveUpdate,  'MoveTask'  )
        taskMgr.add( self.jumpUpdate,  'JumpTask'  )


    def loadModel(self):
        """ make the nodepath for player """
        self.player = NodePath('player')
        self.player.reparentTo(render)
        self.player.setPos(0,0,2)
        self.player.setScale(.05)


    def setUpCamera(self):
        """ puts camera at the players node """
        pl =  base.cam.node().getLens()
        pl.setFov(self.CameraFOV)
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
        base.accept( "space",    self.setKey, [ "space", 1  ] )
        base.accept( "space-up", self.setKey, [ "space", 0  ] )

        base.accept( "w",    self.setKey, [ "w", 1  ] )
        base.accept( "w-up", self.setKey, [ "w", 0  ] )
        base.accept( "s",    self.setKey, [ "s", 1  ] )
        base.accept( "s-up", self.setKey, [ "s", 0  ] )
        base.accept( "a",    self.setKey, [ "a", 1  ] )
        base.accept( "a-up", self.setKey, [ "a", 0  ] )
        base.accept( "d",    self.setKey, [ "d", 1  ] )
        base.accept( "d-up", self.setKey, [ "d", 0  ] )


    def setKey( self, key, value ):
        self.KeyMap[ key ] = value


    def mouseUpdate(self,task):

        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()

        if base.win.movePointer( 0, base.win.getXSize()/2, base.win.getYSize()/2 ):
            self.player.setH( self.player.getH() - ( x - base.win.getXSize() / 2 ) * self.MouseSensitivity )
            pitch = base.camera.getP() - ( y - base.win.getYSize() / 2 ) * self.MouseSensitivity
            if pitch < -self.PitchMax: pitch = -self.PitchMax
            elif pitch > self.PitchMax: pitch = self.PitchMax
            base.camera.setP( pitch )

        return task.cont


    def moveUpdate(self,task):

        if self.Jumping == False:

            if self.KeyMap["w"] == 1:
                self.Walk = self.FORWARD
            elif self.KeyMap["s"] == 1:
                self.Walk = self.BACKWARD
            else:
                self.Walk = self.STOP

            if self.KeyMap["a"] == 1:
                self.Strafe = self.LEFT
            elif self.KeyMap["d"] == 1:
                self.Strafe = self.RIGHT
            else:
                self.Strafe = self.STOP

        self.player.setPos( self.player, self.Walk   * self.Speed * globalClock.getDt() )
        self.player.setPos( self.player, self.Strafe * self.Speed * globalClock.getDt() )

        if self.Walk == self.FORWARD or self.Walk == self.BACKWARD:

            base.camera.setR( base.camera.getR() + self.CameraCurRoll )
            self.CameraCurRoll += self.CameraRollDt * globalClock.getDt()

            if self.CameraCurRoll > self.CameraMaxRoll:
                self.CameraCurRoll = self.CameraMaxRoll
                self.CameraRollDt *= -1
            elif self.CameraCurRoll < -self.CameraMaxRoll:
                self.CameraCurRoll = -self.CameraMaxRoll
                self.CameraRollDt *= -1

        else:
            base.camera.setR(0)

        if self.Jumping == True:
            base.camera.setR(0)

        return task.cont


    def jumpUpdate(self,task):

        # get the highest Z from the down casting ray
        highestZ = -1000
        for i in range( self.playerGroundHandler.getNumEntries() ):
            entry = self.playerGroundHandler.getEntry(i)
            z = entry.getSurfacePoint(render).getZ()
            if z > highestZ and entry.getIntoNode().getName() == "Cube":
                highestZ = z

        # gravity effects and jumps
        self.player.setZ( self.player.getZ() + self.CurJumpMomentum * globalClock.getDt() )
        self.CurJumpMomentum -= self.JumpMultiplier * globalClock.getDt()

        zdif = self.player.getZ() - highestZ

        if zdif >= 0.35:
            self.Jumping = True
        elif zdif < 0.3 or ( zdif < 0.35 and self.Jumping == False ):
            self.player.setZ( highestZ + 0.3 )
            self.CurJumpMomentum = 0
            self.Jumping = False

        if self.KeyMap["space"] == 1 and self.Jumping == False:
            self.CurJumpMomentum = self.MaxJumpMomentum
            self.Jumping = True

        return task.cont
