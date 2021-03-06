from pandac.PandaModules import *
import math
import datetime
from direct.gui.OnscreenText import OnscreenText

from PlayerStates import State as pState
from GameStates import State as gState

class Player( object ):

    # To keep track of which keys are pressed
    KeyMap = { "w":0, "a":0, "s":0, "d":0, "space":0, "r":0 }

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
        self.createCollisions()
        self.attachControls()
        
        self.savedCheckPoint = -1
        self.savedPos = ( -34, 30, 3 )
        self.savedTime = datetime.timedelta(seconds=0)
                
        taskMgr.add( self.mouseUpdate, 'MouseTask' )
        taskMgr.add( self.moveUpdate,  'MoveTask'  )
        taskMgr.add( self.jumpUpdate,  'JumpTask'  )
        taskMgr.add( self.fallingUpdate, 'FallingTask'  )


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


    def createCollisions( self ):
        """ create a collision solid and rays for the player """
        self.playerCol = CollisionNode( 'player' )
        self.playerCol.addSolid( CollisionSphere( 0, 0, 0, 3 ) )
        self.playerColNp = self.player.attachNewNode( self.playerCol )
        base.cTrav.addCollider( self.playerColNp, base.pusher )
        base.pusher.addCollider( self.playerColNp, self.player, base.drive.node() )

        # init player's floor collisions
        self.groundRay = CollisionRay()
        self.groundRay.setOrigin( 0, 0, -.2 )
        self.groundRay.setDirection( 0, 0, -1 )

        self.groundCol = CollisionNode( 'playerGroundRay' )
        self.groundCol.addSolid( self.groundRay )
        self.groundCol.setFromCollideMask( BitMask32.bit(0) )
        self.groundCol.setIntoCollideMask( BitMask32.allOff() )

        self.groundColNp = self.player.attachNewNode( self.groundCol )
        self.groundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider( self.groundColNp, self.groundHandler )

        # init player's forward collisions
        self.forwardRay = CollisionRay()
        self.forwardRay.setOrigin( 0, 0, -.2 )
        self.forwardRay.setDirection( 0, 1, 0 )

        self.forwardCol = CollisionNode( 'playerForwardRay' )
        self.forwardCol.addSolid( self.forwardRay )
        self.forwardCol.setFromCollideMask( BitMask32.bit(0) )
        self.forwardCol.setIntoCollideMask( BitMask32.allOff() )

        self.forwardColNp = self.player.attachNewNode( self.forwardCol )
        self.forwardHandler = CollisionHandlerQueue()
        base.cTrav.addCollider( self.forwardColNp, self.forwardHandler )

        # Uncomment this line to see the collision rays
        #self.groundColNp.show()
        #self.forwardColNp.show()

        # Uncomment this line to show a visual representation of the 
        # collisions occuring
        #base.cTrav.showCollisions(render)
       

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
        base.accept( "l", self.game.checkForRecord )
        #base.accept( "l" , self.reloadLastCheckPoint)


    def setKey( self, key, value ):

        if key == "space" and value == 0 and self.CurState == pState.JUMPING:
            self.ReadyToDoubleJump = True

        self.KeyMap[ key ] = value


    def roll( self ):

        if self.CurState != pState.ROLLING:

            self.CurState = pState.ROLLING
            if  ( self.CurSpeed >= 0 ): self.CurSpeed = 10
            elif( self.CurSpeed <  0 ): self.CurSpeed = -5
            self.CurStrafeSpeed = 0
            self.RollDegrees    = -base.camera.getP()
            self.RollCurHeight  = 0
            base.camera.setZ(0)


    def bad_landing( self ):

        if self.CurState != pState.BAD_LANDING:

            self.CurState = pState.BAD_LANDING
            self.CurSpeed         = 0
            self.CurStrafeSpeed   = 0
            self.LandingCurHeight = 0
            self.LandingCurDt     = self.LandingFastDt
            base.camera.setZ(0)


    def stunned( self ):

        if self.CurState != pState.STUNNED:

            self.CurState = pState.STUNNED
            self.CurSpeed         = -5
            self.CurStrafeSpeed   = 0
            self.StunnedCount     = 0
            self.StunnedCurHeight = 0
            base.camera.setZ(0)


    def verifyGroundCollisions( self ):
        #print self.player.getPos()    

        # Get the highest Z from the down casting ray
        highestZ = -1000
        for i in range( self.groundHandler.getNumEntries() ):
            entry = self.groundHandler.getEntry( i )
            z = entry.getSurfacePoint( render ).getZ()
            if z > highestZ and ("platform" in entry.getIntoNode().getName() or "waypoint" in entry.getIntoNode().getName()):
                highestZ = z
                
                # cehck if the player have touched the last checkpoint in game
                if self.currentCheckPoint == self.lastCheckPoint:
                    
                    self.game.checkForRecord()
                                
                
                if "waypoint"+str(self.currentCheckPoint) in entry.getIntoNode().getName():
                    #print "z " + str(z)
                    #print "player " + str(self.player.getZ())
                    dz = abs(z - self.player.getZ())
                    #print "dz " + str(dz)
                    if dz < 0.3:
                        if self.savedCheckPoint != self.currentCheckPoint:
                            self.saveCheckPoint()
                            self.currentCheckPoint+= 1
                            #obj = render.find("**/waypoint"+str(self.currentCheckPoint))
                            #print obj.getMaterial()
                            #obj.setMaterial(self.myMaterial)
                            #print obj.getMaterial()
                    
                           
        return highestZ


    def verifyForwardCollisions( self ):

        # Get the closest obstacle from the forward ray
        px = self.player.getX()
        py = self.player.getY()

        lowestDist = 1000
        for i in range( self.forwardHandler.getNumEntries() ):

            entry = self.forwardHandler.getEntry( i )
            if "platform" in entry.getIntoNode().getName():

                point = entry.getSurfacePoint( render )
                x = point.getX()
                y = point.getY()
                dist = math.sqrt( (px-x)*(px-x) + (py-y)*(py-y) )

                if dist < lowestDist:
                    lowestDist = dist
                                                        

        return lowestDist


    def applyAcceleration( self ):

        lowestDist = self.verifyForwardCollisions()

        # Only let player alter his course if not jumping (he can still alter it by moving the camera, though)
        if pState.canAccelerate( self.CurState ) == True:

            # Accelerate forward
            if self.KeyMap["w"] == 1:

                # Can't accelerate into a brick wall
                if lowestDist > 0.24:

                    if self.CurSpeed < 0:
                        self.CurSpeed += self.ActiveDeaccel * globalClock.getDt()
                    else:
                        self.CurSpeed += self.Accel * globalClock.getDt()

                    if self.CurSpeed > self.MaxSpeed:
                        self.CurSpeed = self.MaxSpeed

                elif self.CurSpeed > 30:
                    self.stunned()

                else:
                    self.CurSpeed = 0

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
        elif pState.inMidAir( self.CurState ) == True:

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
                                        
        if self.CurSpeed > 0 and self.CurState == pState.RUNNING: 
            self.game.skyRunnerInstance.soundManager.soundWalking.setVolume(1)
        else:
            self.game.skyRunnerInstance.soundManager.soundWalking.setVolume(0)
			
        self.game.skyRunnerInstance.soundManager.soundWalking.setPlayRate(self.CurSpeed*0.025)
                    
    def cameraEffects( self ):

        if self.CurState == pState.RUNNING:

            # Shake camera when player is running
            if self.CurSpeed != 0:

                # The camera will shake most when MaxSpeed is reached
                relSpeed = abs( self.CurSpeed / self.MaxSpeed )

                base.camera.setX( base.camera.getX() + self.CameraCurShake )
                base.camera.setR( base.camera.getR() + self.CameraCurShake )

                self.CameraCurShake += self.CameraShakeDt * relSpeed * globalClock.getDt()

                if self.CameraCurShake > self.CameraMaxShake * relSpeed:
                    self.CameraCurShake = self.CameraMaxShake * relSpeed
                    self.CameraShakeDt *= -1
                elif self.CameraCurShake < -self.CameraMaxShake * relSpeed:
                    self.CameraCurShake = -self.CameraMaxShake * relSpeed
                    self.CameraShakeDt *= -1

        # Don't shake camera when player is in mid-air
        elif pState.inMidAir( self.CurState ) == True:

            self.CameraCurShake = 0
            base.camera.setX(0)
            base.camera.setR(0)

        elif self.CurState == pState.ROLLING:

            if self.RollDegrees < 360:

                self.RollDegrees += self.RollCamDt * globalClock.getDt()
                if self.RollDegrees > 360: self.RollDegrees = 360

                if self.CurSpeed >= 0:
                    base.camera.setP( -self.RollDegrees )
                else:
                    base.camera.setP( self.RollDegrees )

            if self.RollDegrees > 210:

                base.camera.setZ( base.camera.getZ() - self.RollCurHeight )
                self.RollCurHeight += self.RollPosDt * globalClock.getDt()

                if self.RollCurHeight > self.RollMaxHeight:
                    self.RollCurHeight = -self.RollMaxHeight

                if base.camera.getZ() > 0:
                    self.CurState = pState.RUNNING
                    base.camera.setP(0)
                    base.camera.setZ(0)

        elif self.CurState == pState.BAD_LANDING:

            base.camera.setZ( base.camera.getZ() - self.LandingCurHeight )
            base.camera.setR( base.camera.getR() - self.LandingCurHeight )
            base.camera.setP( base.camera.getP() - self.LandingCurHeight * 8 )
            self.LandingCurHeight += self.LandingCurDt * globalClock.getDt()

            if self.LandingCurHeight > self.LandingMaxHeight:
                self.LandingCurHeight = 0
                self.LandingCurDt = self.LandingSlowDt

            if base.camera.getZ() > 0:
                self.CurState = pState.RUNNING
                base.camera.setZ(0)
                base.camera.setR(0)

        elif self.CurState == pState.STUNNED:

            base.camera.setP( base.camera.getP() - self.StunnedCurHeight )
            self.StunnedCurHeight += self.StunnedDt * globalClock.getDt()

            increment = False
            if base.camera.getP() > self.StunnedMaxHeight:
                base.camera.setP( self.StunnedMaxHeight )
                increment = True
            elif base.camera.getP() < -self.StunnedMaxHeight:
                base.camera.setP( -self.StunnedMaxHeight )
                increment = True

            if increment == True:
                self.StunnedCount += 1
                self.StunnedCurHeight = 0
                self.StunnedDt *= -1

            if self.StunnedCount > 3:
                self.CurState = pState.RUNNING


    def applyJump( self ):

        # Player wants to jump
        if self.KeyMap["space"] == 1:

            if self.CurState == pState.RUNNING:
                
                self.CurJumpMomentum = self.MaxJumpMomentum
                self.CurState = pState.JUMPING
                self.game.skyRunnerInstance.soundManager.soundWalking.setVolume(0.0)
                self.game.skyRunnerInstance.soundManager.soundJump.play()

                # Jumping in a certain direction can give you horizontal momentum, at the price of vertical momentum
                if self.KeyMap["w"] == 0:
                    if self.KeyMap["s"] == 1:

                        self.CurJumpMomentum *= 0.8
                        self.CurStrafeSpeed *= 0.1
                        if self.CurSpeed > 0:
                            self.CurSpeed = - self.MaxSpeed / 2 + self.CurSpeed * 0.25
                        else:
                            self.CurSpeed = - self.MaxSpeed / 2

                    elif self.KeyMap["d"] == 1:

                        self.CurJumpMomentum *= 0.8
                        self.CurSpeed *= 0.1
                        self.CurStrafeSpeed = self.MaxStrafeSpeed * 1.5

                    elif self.KeyMap["a"] == 1:

                        self.CurJumpMomentum *= 0.8
                        self.CurSpeed *= 0.1
                        self.CurStrafeSpeed = -self.MaxStrafeSpeed * 1.5

            elif self.ReadyToDoubleJump == True:
                self.game.skyRunnerInstance.soundManager.soundJump.play()
                self.ReadyToDoubleJump = False
                self.CurJumpMomentum = self.MaxJumpMomentum
                self.CurState = pState.DOUBLE_JUMPING
                #self.FallHeight = 0


    def mouseUpdate( self, task ):

        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()

        if base.win.movePointer( 0, base.win.getXSize()/2, base.win.getYSize()/2 ):

            if pState.canMoveCamera( self.CurState ) == True:

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

        # Apply camera shake effects
        self.cameraEffects()

        return task.cont


    def jumpUpdate( self, task ):

        # Gravity effects and jumps
        if self.CurJumpMomentum < 0:
            self.FallHeight -= self.CurJumpMomentum * globalClock.getDt()

        self.player.setZ( self.player.getZ() + self.CurJumpMomentum * globalClock.getDt() )
        self.CurJumpMomentum -= self.JumpMultiplier * globalClock.getDt()

        highestZ = self.verifyGroundCollisions()
        zdif = self.player.getZ() - highestZ

        # Detecting a fall
        if zdif >= 0.333 and self.CurState == pState.RUNNING:

            self.CurState = pState.FALLING

        # Detecting the end of a fall/jump, or preventing a really small one
        elif zdif < 0.3 or ( zdif < 0.333 and self.CurState == pState.RUNNING ):

            self.player.setZ( highestZ + 0.3 )
            self.CurJumpMomentum = 0

            if pState.inMidAir( self.CurState ) == True:

                if self.KeyMap["r"] == 1:
                    self.roll()
                elif self.FallHeight > self.FallHeightThreshold:
                    self.bad_landing()
                else:
                    self.CurState = pState.RUNNING
                    self.game.skyRunnerInstance.soundManager.soundWalking.setVolume(1) 

                self.ReadyToDoubleJump = False
                self.FallHeight = 0

        # If the player wants to jump and meets the requirements, apply it
        self.applyJump()

        return task.cont
    
    def fallingUpdate(self, task):
        
        if self.player.getZ() < -4:
            print "a"
            if self.falling == False:
                print "b"
                self.falling = True 
                self.game.skyRunnerInstance.soundManager.screamSound.play()
            else:
                print "c"
                if self.game.skyRunnerInstance.soundManager.screamSound.getTime() >= 3:
                    print "d"
                    self.falling = False
                    self.respawn()
                            
        return task.cont
    
    def saveCheckPoint( self ):
        self.savedCheckPoint = self.currentCheckPoint
        self.savedPos = self.player.getPos()
        self.savedTime = self.game.displayTime
        
    def reloadLastCheckPoint( self ): 
        self.currentCheckPoint = self.savedCheckPoint+1
        self.player.setPos(self.savedPos)
        self.game.startTime = datetime.datetime.today()
        self.game.lastTimeStop = self.savedTime
        self.resetPlayerVariables()
    
    def respawn( self ):
        self.game.skyRunnerInstance.soundManager.screamSound.stop()
        if self.vidas > 1:
            self.vidas = self.vidas - 1
            self.game.vVidasOn[self.vidas].hide()
            self.game.vVidasOff[self.vidas].show()
            self.reloadLastCheckPoint()
        else:
            self.game.vVidasOn[self.vidas-1].hide()
            self.game.vVidasOff[self.vidas-1].hide()
#            OnscreenText(text = "GAME OVER", style = 1, fg = ( 1, 0, 0, 1 ),
#                                pos = ( -1.33, .25 ), align = TextNode.ALeft, scale = .8 )
    
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