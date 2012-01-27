import sys,os 

#Shaders
from pandac.PandaModules import loadPrcFileData

from direct.showbase.ShowBase import ShowBase 
from panda3d.core import Shader,TransparencyAttrib, AntialiasAttrib, DirectionalLight, AmbientLight 
from panda3d.core import Vec4 , Vec3

from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

 


loadPrcFileData("", "framebuffer-multisample 1")


class TestApp(ShowBase): 
    def __init__(self): 
        ShowBase.__init__(self) 

        render.setAntialias(AntialiasAttrib.MMultisample,1)        
        self.accept("escape", sys.exit) 
        

        self.torus1= self.loader.loadModel('../blender/level.Sources/rosquinha.egg')
        self.torus1.reparentTo(self.render)
        self.torus1.setTwoSided(True)
        shader = Shader.load(Shader.SLGLSL, 'simple.vert', 'simple.frag')
        self.torus1.setTransparency(TransparencyAttrib.MAlpha)
#        self.torus.setSmoothShading() 
        self.torus1.setShader(shader);
         
        self.torus1.setPos(0.0,0.0,0.0)
        #self.torus1.setShaderAuto()
        self.stepTask = taskMgr.add(self.timer, "timer")
        self.stepTask.last = 0
        
        base.trackball.node().setPos(0, 10, 0)
        
        self.setUpLights()

    def initPlayer( self ):
        """ loads the player and creates all the controls for him"""
        self.player = Player()
                
    def setUpLights(self):
        
        self.ambientLight = render.attachNewNode(AmbientLight('ambient light'))
        self.ambientLight.node().setColor(Vec4(0.3, 0.3, 0.3, 1))
        
        self.solarBeam = base.cam.attachNewNode(DirectionalLight("Light"))
        self.solarBeam.node().setLens(base.cam.node().getLens())

        render.setLight(self.solarBeam)
        render.setLight(self.ambientLight)
        render.setAntialias(AntialiasAttrib.MAuto)
            
    def timer(self, task):
        return task.cont  
          
         
app = TestApp() 
app.run()
