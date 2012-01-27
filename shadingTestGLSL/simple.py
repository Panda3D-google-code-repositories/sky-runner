import sys 

#Shaders
from pandac.PandaModules import loadPrcFileData

from direct.showbase.ShowBase import ShowBase 
from panda3d.core import Shader, Vec4 ,AntialiasAttrib , TransparencyAttrib , VBase3
from panda3d.core import DirectionalLight, AmbientLight

loadPrcFileData("", "framebuffer-multisample 1")

class TestApp(ShowBase): 
    def __init__(self): 
        ShowBase.__init__(self) 

        #render.setAntialias(AntialiasAttrib.MMultisample,1)        
        self.accept("escape", sys.exit) 
        
        
        #node = self.loader.loadModel('../blender/sky/box-2.49.egg') 
        self.cube = self.loader.loadModel('levelDesign-01.egg')
        self.cube.reparentTo(self.render)
        self.cube.setTransparency(TransparencyAttrib.MAlpha) 
        #self.cube.setAlphaScale(0.2) 
        
        
        sky = self.loader.loadModel('../blender/sky.Sources/skydomeblendSmooth.egg')
        sky.reparentTo(self.render)
        
        
        shader = Shader.load(Shader.SLGLSL, 'glass.vert', 'glass.frag') 
        #self.cube.setShader(shader) 
        #self.cube.setShaderAuto()
                
        self.stepTask = taskMgr.add(self.timer, "timer")
        self.stepTask.last = 0    
                
#        base.disableMouse() 

        
        self.ambientLight = render.attachNewNode(AmbientLight('ambient light'))
        self.ambientLight.node().setColor(Vec4(0.3, 0.3, 0.3, 1))
        
        self.solarBeam = base.cam.attachNewNode(DirectionalLight("Light"))
        self.solarBeam.node().setLens(base.cam.node().getLens())

        render.setLight(self.solarBeam)
        render.setLight(self.ambientLight)
        #render.setShaderAuto()
        #render.setAntialias(AntialiasAttrib.MAuto)

 
        base.trackball.node().setPos(0, 5, 0)
        
    def timer(self, task):
        
        self.cube.setShaderInput("LightPosition", VBase3(base.trackball.node().getHpr()))
        
        return task.cont        
        
app = TestApp() 
app.run()
