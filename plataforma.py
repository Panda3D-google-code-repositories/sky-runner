import random
from direct.showbase.DirectObject import DirectObject

from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import BitMask32

from direct.gui.OnscreenText import OnscreenText

from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletGhostNode
 
#modulo da classe Avatar
class Plataformas(DirectObject):
    def __init__(self,parent,worldNP,world,nPlataformas):
        self.numeroPlataformas = nPlataformas
        self.parent = parent
        self.cores = {1: Vec4(1, 0, 0, 1), 2: Vec4(0, 1, 0, 1), 3: Vec4(0, 0, 1, 1), 4: Vec4(1, 1, 0, 1), 5: Vec4(1, 0, 1, 1), 6: Vec4(0, 1, 1, 1), 7: Vec4(1, 1, 1, 1), 8: Vec4(0, 0, 0, 1)}
        
        self.estrada = BulletBoxShape(Vec3(50.0, 300.0, 0.3))
        
        self.worldNP = worldNP
        self.world = world
        
        self.estradaNp = worldNP.attachNewNode(BulletRigidBodyNode('Estrada'))
        self.estradaNp.node().addShape(self.estrada)
        self.estradaNp.setPos(0, 40, -1.3)
        self.estradaNp.setH(0.0)
        self.estradaNp.setCollideMask(BitMask32.allOn())
        model = loader.loadModel('models/cubo.egg')
        model.setScale(50,300,0.1)
        #model.flattenLight()
        model.reparentTo(self.estradaNp)

        world.attachRigidBody(self.estradaNp.node())
        
        self.pilar = BulletBoxShape(Vec3(30, 30, 80))
        self.pilarNp = worldNP.attachNewNode(BulletGhostNode('pilar'))
        self.ghostPilar = self.pilarNp.node()
        self.pilarNp.node().addShape(self.pilar)
        self.pilarNp.setPos(10, 10, 70)
        self.pilarNp.setCollideMask(BitMask32.allOn())
        model = loader.loadModel('models/cubo.egg')
        model.setScale(20,20,75)
        #model.flattenLight()
        model.reparentTo(self.pilarNp)
        
        world.attachGhost(self.ghostPilar)
        
        self.geraPlataformas()
        
        taskMgr.add(self.checkGhost, 'checkGhost')
    
    def checkGhost(self, task):
      ghost = self.pilarNp.node()
      for node in ghost.getOverlappingNodes():
        if isinstance(node,BulletCharacterControllerNode):
            taskMgr.remove ('Timer')
            taskMgr.remove('updateWorld')
            OnscreenText('YOU WIN',scale = 0.4, fg= (0,1,0,1))
     
      return task.cont
 

        
    def geraPlataformas(self):
        for i in range(self.numeroPlataformas):
            self.criaPlataforma()
    
    def criaPlataforma(self):
        cor = self.cores[random.randint(1, 8)]

        x = random.randint(-15, 15)
        y = random.randint(-200, 200)
        z = random.randint(0, 30)
        
        c = random.random()*10+3
        l = random.random()*10+3
        a = random.random()
        
        shape = BulletBoxShape(Vec3(l, c, a))
        
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
        #np.node().setMass(1.0)
        np.node().addShape(shape)
        np.setPos(x, y, z)
        np.setH(random.random()*360)
        np.setCollideMask(BitMask32.allOn())
        model = loader.loadModel('models/cubo.egg')
        model.setScale(l,c,a)
        #model.flattenLight()
        model.reparentTo(np)

        model.setColor(1.0,0.0,0.0,1.0)

        self.world.attachRigidBody(np.node())