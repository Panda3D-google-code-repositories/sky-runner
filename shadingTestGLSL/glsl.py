import sys,os 

#Shaders
from pandac.PandaModules import loadPrcFileData

from direct.showbase.ShowBase import ShowBase 
from panda3d.core import Shader,TransparencyAttrib, AntialiasAttrib, DirectionalLight, AmbientLight 
from panda3d.core import Vec4 , Vec3

from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

 

#loadPrcFileData("", "prefer-parasite-buffer #f")
loadPrcFileData("", "framebuffer-multisample 1")
loadPrcFileData("", "multisamples 2")

class TestApp(ShowBase): 
    def __init__(self): 
        ShowBase.__init__(self) 


        render.setAntialias(AntialiasAttrib.MMultisample,1)        
        self.accept("escape", sys.exit) 
        
                 
        self.torus = self.loader.loadModel('../blender/level.Sources/levelDesign-01.egg')
        self.torus.reparentTo(self.render)
        self.torus.setTwoSided(True)
         
        self.torus.setPos(0.0,0.0,5.0)
        #shader = Shader.load(Shader.SLGLSL, 'simple.vert', 'simple.frag')
        self.torus.setTransparency(TransparencyAttrib.MAlpha)
         
#        self.torus.setSmoothShading() 
        #self.torus.setShader(shader);
        
        
        
#        #frag

 #       self.torus.setShaderInput("Edge", 0.25)
#        self.torus.setShaderInput("Phong", 0.1)
#        self.torus.setShaderInput("Fuzz", 0.1)
#        self.torus.setShaderInput("PhongColor", Vec3(0.0, 0.0, 1.0))
#        self.torus.setShaderInput("DiffuseColor", Vec3( 0.0, 0.0, 1.0))
        

        self.torus1= self.loader.loadModel('torus.egg')
        self.torus1.reparentTo(self.render)
        self.torus1.setTwoSided(True)
         
        self.torus1.setPos(0.0,0.0,10.0)
        self.torus1.setShaderAuto()
        shader = Shader.load(Shader.SLGLSL, 'simple.vert', 'simple.frag')
        self.torus1.setTransparency(TransparencyAttrib.MAlpha)
#        self.torus.setSmoothShading() 
        self.torus1.setShader(shader);
        
        
        
#        #frag

#        self.torus.setShaderInput("Edge", 0.25)
#        self.torus.setShaderInput("Phong", 0.1)
#        self.torus.setShaderInput("Fuzz", 0.1)
#        self.torus.setShaderInput("PhongColor", Vec3(0.0, 0.0, 1.0))
#        self.torus.setShaderInput("DiffuseColor", Vec3( 0.0, 0.0, 1.0))
                
 
        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        pandaPosInterval1 = self.torus.posInterval(13,
                                                        Point3(0, -10, 0),
                                                        startPos=Point3(0, 10, 0))
        pandaPosInterval2 = self.torus.posInterval(13,
                                                        Point3(0, 10, 0),
                                                        startPos=Point3(0, -10, 0))
        pandaHprInterval1 = self.torus.hprInterval(3,
                                                        Point3(180, 0, 0),
                                                        startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = self.torus.hprInterval(3,
                                                        Point3(0, 0, 0),
                                                        startHpr=Point3(0, 360, 0))
 
        # Create and play the sequence that coordinates the intervals.
        self.torusPace = Sequence( pandaHprInterval2, name="pandaPace")
        self.torusPace.loop()
            
        #node = self.loader.loadModel('../blender/sky/box-2.49.egg') 
        self.cube = self.loader.loadModel('platform-tex1.egg')
        self.cube.reparentTo(render)
        #self.cube.setTwoSided(True)

        self.cube.setPos(0.0,0.0,0.0)
        self.cube.setShaderAuto()
        #shader = Shader.load(Shader.SLGLSL, 'toon.vert', 'toon.frag')
        #self.cube.setShader(shader);
        #self.cube.setShaderInput("LightPosition", Vec3(0, 0, 0)) 
                
#        self.sky = loader.loadModel('../blender/sky.Sources/skydomeblendSmooth.egg')
#        self.sky.reparentTo(render)
#        self.sky.setLightOff()
                       
              
        #self.cube.setShader(shader) 
                
        self.stepTask = taskMgr.add(self.timer, "timer")
        self.stepTask.last = 0
            
        base.camLens.setNearFar(5,1500)
        base.camLens.setFov(75)
        base.disableMouse()
        
        #base.trackball.node().setPos(0, 10, 0)
        
        self.setUpLights()
        self.initPlayer();

    def initPlayer( self ):
        """ loads the player and creates all the controls for him"""
        self.player = Player()
                
    def setUpLights(self):
    
        #self.solarBeam = render.attachNewNode(DirectionalLight('sun'))
        #self.solarBeam.node().setColor(Vec4(0.7, 0.7, 0.7, 1))
        #self.solarBeam.setHpr(0, 100, 100)
        
        self.ambientLight = render.attachNewNode(AmbientLight('ambient light'))
        self.ambientLight.node().setColor(Vec4(0.3, 0.3, 0.3, 1))
        
        self.solarBeam = base.cam.attachNewNode(DirectionalLight("Light"))
        self.solarBeam.node().setLens(base.cam.node().getLens())
        #base.cam.node().showFrustum()
        
  
#        dLight = DirectionalLight('dLight')
#        dLight.setLens(base.cam.node().getLens())
##        dLight.setColor(Vec4(0.8,0.8,0.75,1))
#        dLightNP = render.attachNewNode(dLight)
#        dLightNP.setHpr(0,-90,0)
#        dLightNP.setPos(0, 0, 60)
#        #dLight.setPoint(Point3(0,0,20))
#        dLight.setShadowCaster(True, 4096, 4096)
#        dLight.showFrustum()
#        dLight.getLens().setFilmSize(4096, 4096)
#        dLight.getLens().setNearFar(10, 750)
#        render.setLight(dLightNP)
        
        # Enable the shader generator for the receiving nodes
        #render.setShaderAuto()
        render.setLight(self.solarBeam)
        render.setLight(self.ambientLight)
        render.setAntialias(AntialiasAttrib.MAuto)
            
    def timer(self, task):
        return task.cont  
          
          
from pandac.PandaModules import *
import math

loadPrcFileData("", "framebuffer-multisample 1")

class State( object ):
    RUNNING, FALLING, JUMPING, DOUBLE_JUMPING, ROLLING, BAD_LANDING, STUNNED = range(7)

    @staticmethod
    def canMoveCamera( state ):
        if( state == State.RUNNING or state == State.FALLING or
            state == State.JUMPING or state == State.DOUBLE_JUMPING ):
            return True
        return False

    @staticmethod
    def canAccelerate( state ):
        if state == State.RUNNING:
            return True
        return False

    @staticmethod
    def inMidAir( state ):
        if state == State.FALLING or state == State.JUMPING or state == State.DOUBLE_JUMPING:
            return True
        return False


class Player( object ):

    # To keep track of which keys are pressed
    KeyMap = { "w":0, "a":0, "s":0, "d":0, "space":0, "r":0, "e":0,"q":0 }

    # Player state
    CurState = State.RUNNING

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
    MaxJumpMomentum = 3 # Higher value results in higher jumps
    JumpMultiplier  = 7 # Higher value will cause player to rise and fall faster
    ReadyToDoubleJump = False

    # Fall variables
    FallHeight          = 0
    FallHeightThreshold = 2.5 # Falling from a height greater than this without rolling will cause a bad landing

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


    def __init__( self ):
        """ inits the player """
        self.loadModel()
        self.setUpCamera()
        self.attachControls()
        taskMgr.add( self.mouseUpdate, 'MouseTask' )
        taskMgr.add( self.moveUpdate,  'MoveTask'  )
       

    def loadModel( self ):
        """ make the nodepath for player """
        self.player = NodePath( 'player' )
        self.player.reparentTo( render )
        self.player.setPos( 0, 0, 10 )
        self.player.setScale( .05 )


    def setUpCamera( self ):
        """ puts camera at the players node """
        pl =  base.cam.node().getLens()
        pl.setFov( self.CameraFOV )
        base.cam.node().setLens( pl )
        base.camera.reparentTo( self.player )
    

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


    def setKey( self, key, value ):

        if key == "space" and value == 0 and self.CurState == State.JUMPING:
            self.ReadyToDoubleJump = True

        self.KeyMap[ key ] = value



 
    def applyAcceleration( self ):

        # Only let player alter his course if not jumping (he can still alter it by moving the camera, though)
        if State.canAccelerate( self.CurState ) == True:
            
            if self.KeyMap["e"] == 1:
                self.player.setZ( self.player, 25*globalClock.getDt() )
                
            elif self.KeyMap["q"] == 1:
                self.player.setZ( self.player, -25*globalClock.getDt() )
            # Accelerate forward
            elif self.KeyMap["w"] == 1:


                    if self.CurSpeed < 0:
                        self.CurSpeed += self.ActiveDeaccel * globalClock.getDt()
                    else:
                        self.CurSpeed += self.Accel * globalClock.getDt()

                    if self.CurSpeed > self.MaxSpeed:
                        self.CurSpeed = self.MaxSpeed

                
            # Accelerate backward
            elif self.KeyMap["s"] == 1:

                if self.CurSpeed > 0:
                    self.CurSpeed -= self.ActiveDeaccel * globalClock.getDt()
                else:
                    self.CurSpeed -= self.Accel * globalClock.getDt()

                if self.CurSpeed < -self.MaxSpeed/2:
                    self.CurSpeed = -self.MaxSpeed/2

            # If not going forward or backward, slow down until speed is 0
            else:

                if self.CurSpeed > 0:
                    self.CurSpeed -= self.PassiveDeaccel * globalClock.getDt()
                    if self.CurSpeed < 0:
                        self.CurSpeed = 0

                elif self.CurSpeed < 0:
                    self.CurSpeed += self.PassiveDeaccel * globalClock.getDt()
                    if self.CurSpeed > 0:
                        self.CurSpeed = 0

            # Accelerate right
            if self.KeyMap["d"] == 1:

                if self.CurStrafeSpeed < 0:
                    self.CurStrafeSpeed += self.ActiveDeaccel * globalClock.getDt()
                else:
                    self.CurStrafeSpeed += self.Accel * globalClock.getDt()

                if self.CurStrafeSpeed > self.MaxStrafeSpeed:
                    self.CurStrafeSpeed = self.MaxStrafeSpeed

            # Accelerate left
            elif self.KeyMap["a"] == 1:

                if self.CurStrafeSpeed > 0:
                    self.CurStrafeSpeed -= self.ActiveDeaccel * globalClock.getDt()
                else:
                    self.CurStrafeSpeed -= self.Accel * globalClock.getDt()

                if self.CurStrafeSpeed < -self.MaxStrafeSpeed:
                    self.CurStrafeSpeed = -self.MaxStrafeSpeed

            # If not going right or left, slow down until speed is 0
            else:

                if self.CurStrafeSpeed > 0:
                    self.CurStrafeSpeed -= self.PassiveDeaccel * globalClock.getDt()
                    if self.CurStrafeSpeed < 0:
                        self.CurStrafeSpeed = 0

                elif self.CurStrafeSpeed < 0:
                    self.CurStrafeSpeed += self.PassiveDeaccel * globalClock.getDt()
                    if self.CurStrafeSpeed > 0:
                        self.CurStrafeSpeed = 0

        # Slowly deaccelerate all speeds while in mid-air
        elif State.inMidAir( self.CurState ) == True:

            if self.CurSpeed > 0:
                self.CurSpeed -= self.AirDeaccel * globalClock.getDt()
                if self.CurSpeed < 0:
                    self.CurSpeed = 0

            elif self.CurSpeed < 0:
                self.CurSpeed += self.AirDeaccel * globalClock.getDt()
                if self.CurSpeed > 0:
                    self.CurSpeed = 0

            if self.CurStrafeSpeed > 0:
                self.CurStrafeSpeed -= self.AirDeaccel * globalClock.getDt()
                if self.CurStrafeSpeed < 0:
                    self.CurStrafeSpeed = 0

            elif self.CurStrafeSpeed < 0:
                self.CurStrafeSpeed += self.AirDeaccel * globalClock.getDt()
                if self.CurStrafeSpeed > 0:
                    self.CurStrafeSpeed = 0



    def mouseUpdate( self, task ):

        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()

        if base.win.movePointer( 0, base.win.getXSize()/2, base.win.getYSize()/2 ):

            if State.canMoveCamera( self.CurState ) == True:

                self.player.setH( self.player.getH() - ( x - base.win.getXSize() / 2 ) * self.MouseSensitivity )

                pitch = base.camera.getP() - ( y - base.win.getYSize() / 2 ) * self.MouseSensitivity
                if pitch < -self.PitchMax: pitch = -self.PitchMax
                elif pitch > self.PitchMax: pitch = self.PitchMax
                base.camera.setP( pitch )

        return task.cont


    def moveUpdate( self, task ):

        # Update player speed
        self.applyAcceleration()

        # Update player position
        self.player.setY( self.player, self.CurSpeed * globalClock.getDt() )
        self.player.setX( self.player, self.CurStrafeSpeed * globalClock.getDt() )


        return task.cont


    
          
        
app = TestApp() 
app.run()
