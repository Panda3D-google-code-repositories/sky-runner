from pandac.PandaModules import *
import direct.directbase.DirectStart
from direct.task import Task

base.disableMouse()

# hide mouse cursor, comment these 3 lines to see the cursor
props = WindowProperties()
props.setCursorHidden(True)
base.win.requestProperties(props)

# dummy node for camera, attach player to it
camparent = render.attachNewNode('camparent')
camparent.reparentTo(render) # inherit transforms
camparent.setEffect(CompassEffect.make(render)) # NOT inherit rotation

# the camera
base.camera.reparentTo(camparent)
base.camera.lookAt(camparent)
base.camera.setY(0) # camera distance from model

# vars for camera rotation
heading = 0
pitch = 0

# camera rotation task
def cameraTask(task):
   global heading
   global pitch
   
   md = base.win.getPointer(0)
   
   x = md.getX()
   y = md.getY()
   
   if base.win.movePointer(0, 300, 300):
      heading = heading - (x - 300) * 0.2
      pitch = pitch - (y - 300) * 0.2
   
   camparent.setHpr(heading, pitch, 0)
   
   if forward == True:
      camparent.setY(base.cam, camparent.getY(base.cam) + 2)
   if reverse == True:
      camparent.setY(base.cam, camparent.getY(base.cam) - 2)
   if left == True:
      camparent.setX(base.cam, camparent.getX(base.cam) - 2)
   if right == True:
      camparent.setX(base.cam, camparent.getX(base.cam) + 2)
   
   return task.cont

taskMgr.add(cameraTask, 'cameraTask')

# movement
forward = False
reverse = False
left = False
right = False

def forward():
   global forward
   forward = True
         
def stopForward():
   global forward
   forward = False

def reverse():
   global reverse
   reverse = True
         
def stopReverse():
   global reverse
   reverse = False

def left():
   global left
   left = True
         
def stopLeft():
   global left
   left = False

def right():
   global right
   right = True
         
def stopRight():
   global right
   right = False

base.accept("mouse3", forward)
base.accept("mouse3-up", forward)
base.accept("w", forward)
base.accept("w-up", stopForward)
base.accept("s", reverse)
base.accept("s-up", stopReverse)
base.accept("a", left)
base.accept("a-up", stopLeft)
base.accept("d", right)
base.accept("d-up", stopRight)