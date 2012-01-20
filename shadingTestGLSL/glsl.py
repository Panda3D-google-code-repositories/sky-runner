import sys 

#Shaders
from pandac.PandaModules import loadPrcFileData

from direct.showbase.ShowBase import ShowBase 
from panda3d.core import Shader, Vec4 ,AntialiasAttrib , TransparencyAttrib , VBase3

loadPrcFileData("", "framebuffer-multisample 1")

class TestApp(ShowBase): 
    def __init__(self): 
        ShowBase.__init__(self) 

        render.setAntialias(AntialiasAttrib.MMultisample,1)        
        self.accept("escape", sys.exit) 
        
        
        #node = self.loader.loadModel('../blender/sky/box-2.49.egg') 
        self.cube = self.loader.loadModel('paralele-2.49.egg')
        self.cube.reparentTo(self.render)
        self.cube.setTransparency(TransparencyAttrib.MAlpha) 
        
                #node = self.loader.loadModel('../blender/sky/box-2.49.egg') 
        self.cube2 = self.loader.loadModel('paralele-2.49.egg')
        self.cube2.reparentTo(self.render)
        self.cube2.setTransparency(TransparencyAttrib.MAlpha) 
        
        self.cube.setPos(0.0,0.0,5.0)
        
        sky = self.loader.loadModel('../blender/sky/skydomeblendSmooth.egg')
        sky.reparentTo(self.render)
        
        
        shader = Shader.load(Shader.SLGLSL, 'glass.vert', 'glass.frag') 
        self.cube.setShader(shader) 
                
        self.stepTask = taskMgr.add(self.timer, "timer")
        self.stepTask.last = 0    
                
#        base.disableMouse() 
 
        base.trackball.node().setPos(0, 5, 0)
        
    def timer(self, task):
        
        self.cube.setShaderInput("LightPosition", VBase3(base.trackball.node().getHpr()))
        
        return task.cont        
        
app = TestApp() 
app.run()
