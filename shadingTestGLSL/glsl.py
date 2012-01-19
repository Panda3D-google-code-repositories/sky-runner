import sys 
from direct.showbase.ShowBase import ShowBase 
from panda3d.core import Shader 

class TestApp(ShowBase): 
    def __init__(self): 
        ShowBase.__init__(self) 
        
        self.accept("escape", sys.exit) 
        
        node = self.loader.loadModel('rawCube') 
        node.reparentTo(self.render) 
        
        shader = Shader.load(Shader.SLGLSL, 'simple.vert', 'simple.frag') 
        node.setShader(shader) 
        
#        base.disableMouse() 
#        self.camera.setPos(0, -10, 0) 
        base.trackball.node().setPos(0, 10, 0)
        
app = TestApp() 
app.run()