import sys
import preload
import datetime

from direct.actor.Actor import Actor

import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState

from direct.gui.OnscreenText import OnscreenText 

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32
from panda3d.core import Filename
from panda3d.core import PNMImage

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode

from avatar import Avatar
from plataforma import Plataformas

class Game(DirectObject):

  def __init__(self):
    base.setBackgroundColor(0.0, 0.0, 0.6, 1)
    
    base.setFrameRateMeter(True)
    
    # Light
    alight = AmbientLight('ambientLight')
    alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
    alightNP = render.attachNewNode(alight)

    dlight = DirectionalLight('directionalLight')
    dlight.setDirection(Vec3(1, 1, -1))
    dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
    dlightNP = render.attachNewNode(dlight)

    render.clearLight()
    render.setLight(alightNP)
    render.setLight(dlightNP)

    # Input
    self.accept('escape', self.doExit)
    self.accept('r', self.doReset)
    self.accept('f1', self.toggleWireframe)
    self.accept('f2', self.toggleTexture)
    self.accept('f3', self.toggleDebug)
    self.accept('f5', self.doScreenshot)
    self.accept('f6', self.doRoda)

    # Task
    taskMgr.add(self.update, 'updateWorld')

    # Physics
    self.setup()

  # _____HANDLER_____

  def doExit(self):
    self.cleanup()
    sys.exit(1)

  def doReset(self):
    self.cleanup()
    self.setup()

  def toggleWireframe(self):
    base.toggleWireframe()

  def toggleTexture(self):
    base.toggleTexture()

  def toggleDebug(self):
    if self.debugNP.isHidden():
      self.debugNP.show()
    else:
      self.debugNP.hide()

  def doScreenshot(self):
    base.screenshot('Bullet')

  def doRoda(self):
    self.plataformas.estradaNp.setP(self.plataformas.estradaNp.getP()+1)
  # ____TASK___

  def processInput(self):
    speed = Vec3(0, 0, 0)
    omega = 0.0

    if inputState.isSet('forward'): 
        if self.avatar.speed < 0 :
            self.avatar.speed = self.avatar.speed + 3
        elif self.avatar.speed < 35 : 
            self.avatar.speed = self.avatar.speed + 0.1;
        
        speed.setY( self.avatar.speed)
    
    if inputState.isSet('reverse'): 
        if self.avatar.speed > 0 :
            self.avatar.speed = self.avatar.speed - 3
        elif self.avatar.speed > -15 : 
            self.avatar.speed = self.avatar.speed - 0.1;
        
        speed.setY( self.avatar.speed)
    
    if inputState.isSet('left'):    speed.setX(-5.0)
    if inputState.isSet('right'):   speed.setX( 5.0)
    if inputState.isSet('turnLeft'):  omega =  120.0
    if inputState.isSet('turnRight'): omega = -120.0
    
    if not inputState.isSet('forward') and not inputState.isSet('reverse') and not inputState.isSet('left') and not inputState.isSet('right') and not inputState.isSet('turnLeft') and not inputState.isSet('turnRight'):
        if self.avatar.speed < 0.5 :
            self.avatar.speed = 0
        if not self.avatar.speed == 0 :
            self.avatar.speed = self.avatar.speed + (self.avatar.speed * -0.05)
            speed.setY( self.avatar.speed)
            

    self.avatar.setAngularVelocity(omega)
    self.avatar.setLinearVelocity(speed, True)
    base.camera.setHpr( self.avatar.getH()+180, self.avatar.getP(), 0 )
    base.camera.setPos( self.avatar.getX(), self.avatar.getY(), self.avatar.getZ()+2 )


    if (inputState.isSet('forward')) or (inputState.isSet('reverse')) or (inputState.isSet('left')) or (inputState.isSet('right')):
        if self.avatar.isMoving is False:
            self.avatar.playerNP.loop("run")
            self.avatar.isMoving = True
    else:
        if self.avatar.isMoving:
            self.avatar.playerNP.stop()
            self.avatar.playerNP.pose("walk",5)
            self.avatar.isMoving = False
    
    
  def update(self, task):
    dt = globalClock.getDt()

    self.processInput()
    self.world.doPhysics(dt, 5, 0.005)
    
    heading = base.camera.getH()
    pitch   = base.camera.getP()
    
    #condicao de game over
    if self.avatar.playerNP.getZ(render) < -80: 
        taskMgr.remove('updateWorld')
        taskMgr.remove ('Timer')
        OnscreenText('YOU LOSE',scale = 0.4, fg= (1,0,0,1))
    
    return task.cont

  def cleanup(self):
    self.world = None
    self.worldNP.removeNode()
    
  def timer( self, task ): 
      nowTime = datetime.datetime.today()
      t = nowTime - self.startTime
      s = str(t).split(':')
      s2 = s[2].split('.')
      if len(s2) == 1:
       s2.append('00')
      self.clock.setText(':'.join(s[:2])+':'+s2[0]+'\''+s2[1][:1])
      #self.clock.setText( str( int( round( task.time ) ) ) ) 
      return task.cont 
      
  def setup(self):
    self.startTime = datetime.datetime.today()
    self.clock = OnscreenText(scale = .15, mayChange = True, pos= (-0.8,0.87), fg= (1,1,1,1))
    
    self.timerTask = taskMgr.add( self.timer, 'Timer' )
    
    self.worldNP = render.attachNewNode('World')

    self.H_anterior = base.camera.getH()
    
    # World
    self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
    self.debugNP.show()
    self.debugNP.node().setVerbose(False)

    self.world = BulletWorld()
    self.world.setGravity(Vec3(0, 0, -19.81))
    self.world.setDebugNode(self.debugNP.node())

    # Ground
    shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

    np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
    np.node().addShape(shape)
    np.setPos(0, 0, -200)
    np.setCollideMask(BitMask32.allOn())

    self.world.attachRigidBody(np.node())

    # Loading plataformas
    self.plataformas = Plataformas(self,self.worldNP,self.world,50)

    # Loading Character
    self.avatar = Avatar(self.worldNP,self.world)
    
    base.camera.setPos( self.avatar.getX(), self.avatar.getY(), self.avatar.getZ()+1 )
    base.camera.setHpr( self.avatar.getH(), self.avatar.getP(), 0 )

game = Game()
run()

