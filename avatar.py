from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor

from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import ZUp
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.core import BitMask32
from direct.showbase.InputStateGlobal import inputState
 
#modulo da classe Avatar
class Avatar(DirectObject):
    def __init__(self,worldNP,world):
        self.crouching = False
        self.isMoving = False
        self.isJumping = False
        self.speed = 0;

        h = 1.75
        w = 0.4
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

        node = BulletCharacterControllerNode(shape, 0.4, 'Player')
        np = worldNP.attachNewNode(node)
        np.setPos(-2, 0, 14)
        np.setH(45)
        np.setCollideMask(BitMask32.allOn())

        world.attachCharacter(np.node())

        self.player = node # For player control

        self.playerNP = Actor('models/ralph.egg', {
                              'run' : 'models/ralph-run.egg',
                              'walk' : 'models/ralph-walk.egg',
                              'jump' : 'models/ralph-jump.egg'})
        self.playerNP.reparentTo(np)
        self.playerNP.setScale(0.3048) # 1ft = 0.3048m
        self.playerNP.setH(180)
        self.playerNP.setPos(0, 0, -1)
        
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('turnLeft', 'q')
        inputState.watchWithModifiers('turnRight', 'e')
        
        self.accept('space', self.doJump)
        self.accept('c', self.doCrouch)
        
    def doJump(self):
        self.player.setMaxJumpHeight(80)
        self.player.setJumpSpeed(9.6)
        self.player.doJump()
        #self.playerNP.loop("jump")

    def doCrouch(self):
        self.crouching = not self.crouching
        sz = self.crouching and 0.6 or 1.0

        self.player.getShape().setLocalScale(Vec3(1, 1, sz))

        self.playerNP.setScale(Vec3(1, 1, sz) * 0.3048)
        self.playerNP.setPos(0, 0, -1 * sz)
     
    def getX(self):
        return self.playerNP.getX(render)
        
    def getY(self):
        return self.playerNP.getY(render)
        
    def getZ(self):
        return self.playerNP.getZ(render)
        
    def getH(self):
        return self.playerNP.getH(render)
        
    def getP(self):
        return self.playerNP.getP(render)
        
    def getR(self):
        return self.playerNP.getR(render)
        
    def setAngularVelocity(self, omega):
        self.player.setAngularVelocity(omega)
        
    def setLinearVelocity(self, speed, b):
        self.player.setLinearVelocity(speed, b)