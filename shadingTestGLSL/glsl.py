import sys 

#Shaders
from pandac.PandaModules import loadPrcFileData

from direct.showbase.ShowBase import ShowBase 
from panda3d.core import Shader,TransparencyAttrib, AntialiasAttrib, DirectionalLight, AmbientLight 
from panda3d.core import Vec4 , Vec3

from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

 

loadPrcFileData("", "framebuffer-multisample 1")
loadPrcFileData("", "multisamples 2")

class TestApp(ShowBase): 
    def __init__(self): 
        ShowBase.__init__(self) 

        #render.setAntialias(AntialiasAttrib.MMultisample,1)        
        self.accept("escape", sys.exit) 
        
                #node = self.loader.loadModel('../blender/sky/box-2.49.egg') 
        self.torus = self.loader.loadModel('torus.egg')
        self.torus.reparentTo(self.render)
        #self.torus.setTransparency(TransparencyAttrib.MAlpha) 
        self.torus.setPos(0.0,0.0,0.0)
        #self.torus.setShaderAuto()
        shader = Shader.load(Shader.SLGLSL, 'toon.vert', 'toon.frag')
        self.torus.setTransparency(TransparencyAttrib.MAlpha)
        self.torus.setShader(shader);
        #frag
        self.torus.setShaderInput("AmbientMaterial", Vec3(0.4, 0.4, 0.4))
        self.torus.setShaderInput("SpecularMaterial",Vec3(0.5, 0.5,0.5))
        self.torus.setShaderInput("Shininess", 50)
        self.torus.setShaderInput("LightPosition", Vec3(0, 1000, 1000))
        self.torus.setShaderInput("DiffuseMaterial", Vec3( 1.0, 0.75, 0.75))
        
        
 
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
        self.cube = self.loader.loadModel('platform-L.egg')
        self.cube.reparentTo(self.render)
        self.cube.setTransparency(TransparencyAttrib.MAlpha) 
        self.cube.setPos(0.0,0.0,5.0)
        #self.cube.setShaderAuto()
        shader = Shader.load(Shader.SLGLSL, 'toon.vert', 'toon.frag')
        self.cube.setShader(shader);
        #self.cube.setShaderInput("LightPosition", Vec3(0, 0, 0)) 
                
        self.sky = self.loader.loadModel('../blender/sky/skydomeblendSmooth.egg')
        self.sky.reparentTo(self.render)
        self.sky.setLightOff()
                       
              
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
  
        render.setAntialias(AntialiasAttrib.MAuto)
    
    def timer(self, task):
        return task.cont  
          
        
app = TestApp() 
app.run()
