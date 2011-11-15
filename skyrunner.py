import sys
import preload
import direct.directbase.DirectStart

from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState

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
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode

from panda3d.bullet import BulletHeightfieldShape
from avatar import Avatar

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

  # ____TASK___

  def processInput(self):
    speed = Vec3(0, 0, 0)
    omega = 0.0

    if inputState.isSet('forward'): speed.setY( 5.0)
    if inputState.isSet('reverse'): speed.setY(-5.0)
    if inputState.isSet('left'):    speed.setX(-5.0)
    if inputState.isSet('right'):   speed.setX( 5.0)
    if inputState.isSet('turnLeft'):  omega =  120.0
    if inputState.isSet('turnRight'): omega = -120.0

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
    self.world.doPhysics(dt, 10, 0.008)

    #condicao de game over
    if self.avatar.playerNP.getZ(render) < -2: self.doExit()
    
    return task.cont

  def cleanup(self):
    self.world = None
    self.worldNP.removeNode()

  def setup(self):
    self.worldNP = render.attachNewNode('World')

    # World
    self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
    self.debugNP.show()
    self.debugNP.node().setVerbose(False)

    self.world = BulletWorld()
    self.world.setGravity(Vec3(0, 0, -19.81))
    self.world.setDebugNode(self.debugNP.node())

    # Ground
    shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

    #img = PNMImage(Filename('models/elevation2.png'))
    #shape = BulletHeightfieldShape(img, 1.0, ZUp)

    np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
    np.node().addShape(shape)
    np.setPos(0, 0, -10)
    np.setCollideMask(BitMask32.allOn())

    self.world.attachRigidBody(np.node())

    # Box
    shape = BulletBoxShape(Vec3(1.0, 3.0, 0.3))
   
   
    # estrada
    estrada = BulletBoxShape(Vec3(10.0, 300.0, 0.3))
    np = self.worldNP.attachNewNode(BulletRigidBodyNode('Estrada'))
    #np.node().setMass(1.0)
    np.node().addShape(estrada)
    np.setPos(0, 40, -1.3)
    np.setH(0.0)
    np.setCollideMask(BitMask32.allOn())
    model = loader.loadModel('models/cubo.egg')
    model.setScale(10,300,0.15)
    model.flattenLight()
    model.reparentTo(np)

    self.world.attachRigidBody(np.node())
    
    
    np = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
    #np.node().setMass(1.0)
    np.node().addShape(shape)
    np.setPos(3, 4, 2)
    np.setH(20.0)
    np.setCollideMask(BitMask32.allOn())
    model = loader.loadModel('models/cubo.egg')
    model.setScale(5,15,0.15)
    model.flattenLight()
    model.reparentTo(np)

    self.world.attachRigidBody(np.node())
    
    np2 = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
    #np.node().setMass(1.0)
    np2.node().addShape(shape)
    np2.setPos(2, 3, 3)
    np2.setH(10.0)
    np2.setCollideMask(BitMask32.allOn())
    model = loader.loadModel('models/cubo.egg')
    model.setScale(5,15,0.15)
    model.flattenLight()
    model.reparentTo(np2)

    self.world.attachRigidBody(np2.node())

    # Loading Character
    self.avatar = Avatar(self.worldNP,self.world)
    
    base.camera.setPos( self.avatar.getX(), self.avatar.getY(), self.avatar.getZ()+1 )
    base.camera.setHpr( self.avatar.getH(), self.avatar.getP(), 0 )

game = Game()
run()

