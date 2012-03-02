from pandac.PandaModules import *
import math
import datetime
from direct.gui.OnscreenText import OnscreenText

from PlayerStates import State as pState
from GameStates import State as gState

class FlyCamera( object ):

    # To keep track of which keys are pressed
    KeyMap = { "w":0, "a":0, "s":0, "d":0, "space":0, "r":0, "e":0,"q":0 }

    # Player state
    CurState = pState.RUNNING

    # Acceleration variables
    Accel = 60
    AirDeaccel     = 10
    PassiveDeaccel = 200
    ActiveDeaccel  = 400

    # Speed variables
    CurSpeed = 0
    MaxSpeed = 100
    CurStrafeSpeed = 0
    MaxStrafeSpeed = 40

    # Jump variables
    CurJumpMomentum = 0
    MaxJumpMomentum = 5 # Higher value results in higher jumps
    JumpMultiplier  = 7 # Higher value will cause player to rise and fall faster
    ReadyToDoubleJump = False

    # Fall variables
    FallHeight          = 0
    FallHeightThreshold = 5.5 # Falling from a height greater than this without rolling will cause a bad landing

    # Camera variables
    MouseSensitivity = 0.2 # Higher value means faster camera movement
    CameraFOV      = 80
    PitchMax       = 90    # Camera can't look up or down past this value

    # For camera shaking when the player runs
    CameraCurShake = 0
    CameraMaxShake = 0.025 # Higher value results in wider shakes
    CameraShakeDt  = 0.18  # Higher value results in faster shakes

    # For camera effects when the player rolls
    RollDegrees   = 0
    RollCamDt     = 800  # Higher values mean faster rolls (360 degrees)
    RollCurHeight = 0
    RollMaxHeight = 0.09 # Higher value means the camera will descend more
    RollPosDt     = 0.28 # Higher values mean faster rolls (up & down)

    # For camera effects when the player lands badly
    LandingCurHeight = 0
    LandingMaxHeight = 0.17
    LandingFastDt    = 0.60  # How fast the player falls in a bad landing
    LandingSlowDt    = -0.01 # How fast the player gets back up from a bad landing
    LandingCurDt     = 0

    # For camera effects when the player is stunned
    StunnedCount     = 0
    StunnedCurHeight = 0
    StunnedMaxHeight = 5 # Higher value means the camera will descend more
    StunnedDt        = 10.00 # Higher values mean faster shakes
    
    # For checkPoint control

    def __init__( self, gameContext ):
        """ inits the player """
        self.game = gameContext
        self.vidas = 3
        self.falling = False
        
        self.lastCheckPoint = len(render.findAllMatches("**/waypoint*"))
        self.currentCheckPoint = 0;
        
        self.loadModel()
        self.setUpCamera()
#        self.createCollisions()
        self.attachControls()
        
        self.savedCheckPoint = -1
        self.savedPos = ( -34, 30, 3 )
        self.savedTime = datetime.timedelta(seconds=0)
                
        taskMgr.add( self.mouseUpdate, 'MouseTask' )
        taskMgr.add( self.moveUpdate,  'MoveTask'  )
#        taskMgr.add( self.jumpUpdate,  'JumpTask'  )
#        taskMgr.add( self.fallingUpdate, 'FallingTask'  )


    def loadModel( self ):
        """ make the nodepath for player """
        self.flyCamera = NodePath( 'flyCamera' )
        self.flyCamera.reparentTo( render )
        self.flyCamera.setPos( 0, 0, 10 )
        self.flyCamera.setScale( .05 )


    def setUpCamera( self ):
        """ puts camera at the players node """
        pl =  base.cam.node().getLens()
        pl.setFov( self.CameraFOV )
        base.cam.node().setLens( pl )
        base.camera.reparentTo( self.flyCamera )



    def attachControls( self ):
        """ attach key events """
        base.accept( "space",    self.setKey, [ "space", 1 ] )
        base.accept( "space-up", self.setKey, [ "space", 0 ] )
        base.accept( "w",    self.setKey, [ "w", 1 ] )
        base.accept( "w-up", self.setKey, [ "w", 0 ] )
        base.accept( "s",    self.setKey, [ "s", 1 ] )
        base.accept( "s-up", self.setKey, [ "s", 0 ] )
        base.accept( "a",    self.setKey, [ "a", 1 ] )
        base.accept( "a-up", self.setKey, [ "a", 0 ] )
        base.accept( "d",    self.setKey, [ "d", 1 ] )
        base.accept( "d-up", self.setKey, [ "d", 0 ] )
        base.accept( "r",    self.setKey, [ "r", 1 ] )
        base.accept( "r-up", self.setKey, [ "r", 0 ] )
        base.accept( "e",    self.setKey, [ "e", 1 ] )
        base.accept( "e-up", self.setKey, [ "e", 0 ] )
        base.accept( "q",    self.setKey, [ "q", 1 ] )
        base.accept( "q-up", self.setKey, [ "q", 0 ] )
        base.accept( "l", self.game.checkForRecord )
        #base.accept( "l" , self.reloadLastCheckPoint)


    def setKey( self, key, value ):

        if key == "space" and value == 0 and self.CurState == pState.JUMPING:
            self.ReadyToDoubleJump = True

        self.KeyMap[ key ] = value



    def applyAcceleration( self ):

#        lowestDist = self.verifyForwardCollisions()

        # Only let player alter his course if not jumping (he can still alter it by moving the camera, though)
        if pState.canAccelerate( self.CurState ) == True:

            if self.KeyMap["e"] == 1:
                self.flyCamera.setZ( self.flyCamera, 120*globalClock.getDt() )
                
            elif self.KeyMap["q"] == 1:
                self.flyCamera.setZ( self.flyCamera, -120*globalClock.getDt() )
                
            if self.KeyMap["w"] == 1:
                self.flyCamera.setY( self.flyCamera, 120*globalClock.getDt() )
                
            elif self.KeyMap["s"] == 1:
                self.flyCamera.setY( self.flyCamera, -120*globalClock.getDt() )

            if self.KeyMap["d"] == 1:
                self.flyCamera.setX( self.flyCamera, 120*globalClock.getDt() )
                
            elif self.KeyMap["a"] == 1:
                self.flyCamera.setX( self.flyCamera, -120*globalClock.getDt() )
                
                                            

           
  
    def mouseUpdate( self, task ):

        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()

        if base.win.movePointer( 0, base.win.getXSize()/2, base.win.getYSize()/2 ):

            if pState.canMoveCamera( self.CurState ) == True:

                self.flyCamera.setH( self.flyCamera.getH() - ( x - base.win.getXSize() / 2 ) * self.MouseSensitivity )

                pitch = base.camera.getP() - ( y - base.win.getYSize() / 2 ) * self.MouseSensitivity
                if pitch < -self.PitchMax: pitch = -self.PitchMax
                elif pitch > self.PitchMax: pitch = self.PitchMax
                base.camera.setP( pitch )

        return task.cont


    def moveUpdate( self, task ):
        # Update flyCamera speed
        self.applyAcceleration()

        # Update flyCamera position
        self.flyCamera.setY( self.flyCamera, self.CurSpeed * globalClock.getDt() )
        self.flyCamera.setX( self.flyCamera, self.CurStrafeSpeed * globalClock.getDt() )

        return task.cont


    def resetPlayerVariables( self ):
        self.CurSpeed = 0
        self.CurStrafeSpeed = 0
        self.CurJumpMomentum = 0
        self.FallHeight  = 0
        self.CameraCurShake = 0
        self.RollDegrees   = 0
        self.RollCurHeight = 0
        self.LandingCurHeight = 0
        self.LandingCurDt     = 0
        self.StunnedCount     = 0
        self.StunnedCurHeight = 0
        self.CurState = pState.RUNNING