import sys 

#Shaders
from pandac.PandaModules import loadPrcFileData

from direct.showbase.ShowBase import ShowBase 
from panda3d.core import Shader,TransparencyAttrib, AntialiasAttrib, DirectionalLight, AmbientLight 
from panda3d.core import Vec4 , Vec3

 

loadPrcFileData("", "framebuffer-multisample 1")

class TestApp(ShowBase): 
    def __init__(self): 
        ShowBase.__init__(self) 

        #render.setAntialias(AntialiasAttrib.MMultisample,1)        
        self.accept("escape", sys.exit) 
        
            
        #node = self.loader.loadModel('../blender/sky/box-2.49.egg') 
        self.cube = self.loader.loadModel('platform-L.egg')
        self.cube.reparentTo(self.render)
        self.cube.setTransparency(TransparencyAttrib.MAlpha) 
        self.cube.setPos(0.0,0.0,5.0)
        #self.cube.setShaderAuto()
        shader = Shader.load(Shader.SLGLSL, 'gooch.vert', 'gooch.frag')
        self.cube.setShader(shader);
        self.cube.setShaderInput("LightPosition", Vec3(0, 1000, 1000)) 
                
        self.sky = self.loader.loadModel('../blender/sky/skydomeblendSmooth.egg')
        self.sky.reparentTo(self.render)
        self.sky.setShaderAuto()
                       
        
        #self.cube.setShader(shader) 
                
        self.stepTask = taskMgr.add(self.timer, "timer")
        self.stepTask.last = 0    
        base.trackball.node().setPos(0, 10, 0)
        
        self.setUpLights()
        
    def setUpLights(self):
    
        self.solarBeam = render.attachNewNode(DirectionalLight('sun'))
        self.solarBeam.node().setColor(Vec4(0.7, 0.7, 0.7, 1))
        self.solarBeam.setHpr(0, 1000, 1000)
  
        self.ambientLight = render.attachNewNode(AmbientLight('ambient light'))
        self.ambientLight.node().setColor(Vec4(0.3, 0.3, 0.3, 1))
  
        render.setLight(self.solarBeam)
        render.setShaderInput('light', self.solarBeam)
        render.setLight(self.ambientLight)
  
        render.setShaderAuto()
        render.setAntialias(AntialiasAttrib.MAuto)
    
    def timer(self, task):
        return task.cont        
        
app = TestApp() 
app.run()
