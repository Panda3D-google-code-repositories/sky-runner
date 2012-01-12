# Author: Ryan Myers
# Models: Jeff Styers, Reagan Heller
#
# Last Updated: 6/13/2005
#
# This tutorial provides an example of creating a character
# and having it walk around on uneven terrain, as well
# as implementing a fully rotatable camera.

import direct.directbase.DirectStart
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Texture, GeomNode
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
from panda3d.core import WindowProperties
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math

FORWARD_SPEED = 75
BACKWARD_SPEED = 30
STRAFE_SPEED = 45
MOUSE_SENSITIVITY = 0.2

# Function to put instructions on the screen.
def addInstructions( pos, msg ):
    return OnscreenText(text = msg, style = 1, fg = ( 1, 1, 1, 1 ),
                        pos = ( -1.3, pos ), align = TextNode.ALeft, scale = .05 )


# Function to put title on the screen.
def addTitle( text ):
    return OnscreenText(text = text, style = 1, fg = ( 1, 1, 1, 1 ),
                        pos = ( 1.3, -0.95 ), align = TextNode.ARight, scale = .07 )


class World( DirectObject ):

    def __init__( self ):
        
        self.keyMap = { "w":0, "a":0, "s":0, "d":0 }
        base.win.setClearColor( Vec4( 0, 0, 0, 1 ) )

        # Make the mouse invisible, turn off normal mouse controls
        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden( True )
        base.win.requestProperties( props )

        # Post the instructions
        self.title = addTitle( "Sky-Runner Prototype: Mirror's Edge-like Game" )
        self.inst1 = addInstructions( 0.95, "[ESC]: Quit"          )
        self.inst2 = addInstructions( 0.90, "[mouse]: Move Camera" )
        self.inst3 = addInstructions( 0.85, "[C]: Toggle Camera Mode" )
        self.inst4 = addInstructions( 0.80, "[W]: Move Forward"    )
        self.inst5 = addInstructions( 0.75, "[S]: Move Backward"   )
        self.inst6 = addInstructions( 0.70, "[A]: Strafe Left"     )
        self.inst7 = addInstructions( 0.65, "[D]: Strafe Right"    )
        
        # Set up the environment
        #
        # This environment model contains collision meshes.  If you look
        # in the egg file, you will see the following:
        #
        #    <Collide> { Polyset keep descend }
        #
        # This tag causes the following mesh to be converted to a collision
        # mesh -- a mesh which is optimized for collision, not rendering.
        # It also keeps the original mesh, so there are now two copies ---
        # one optimized for rendering, one for collisions.  
        self.environ = loader.loadModel("models/world")
        self.environ.reparentTo(render)
        self.environ.setPos(0,0,0)
        
        # Create the main character, Ralph
        ralphStartPos = self.environ.find("**/start_point").getPos()
        self.ralph = Actor("models/ralph",
                                 {"run":"models/ralph-run",
                                  "walk":"models/ralph-walk"})
        self.ralph.reparentTo(render)
        self.ralph.setScale(.2)
        self.ralph.setPos(ralphStartPos)

        # Create a floater object.  We use the "floater" as a temporary
        # variable in a variety of calculations.
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        # Accept the control keys for movement and rotation
        self.accept( "escape", sys.exit )

        self.accept( "w", self.setKey, [ "w", 1 ] )
        self.accept( "a", self.setKey, [ "a", 1 ] )
        self.accept( "s", self.setKey, [ "s", 1 ] )
        self.accept( "d", self.setKey, [ "d", 1 ] )

        self.accept( "w-up", self.setKey, [ "w", 0 ] )
        self.accept( "a-up", self.setKey, [ "a", 0 ] )
        self.accept( "s-up", self.setKey, [ "s", 0 ] )
        self.accept( "d-up", self.setKey, [ "d", 0 ] )

        self.accept( "c", self.toggleCamera )

        taskMgr.add( self.move, "moveTask" )

        # Game state variables
        self.isMoving = False
        self.fpsMode = True

        # Set up the camera
        if( self.fpsMode == True ):
            base.camera.setPos( self.ralph.getX(), self.ralph.getY(), self.ralph.getZ()+2 )
            base.camera.setHpr( 180, 0, 0 )
        else:
            base.camera.setPos( self.ralph.getX(), self.ralph.getY()+10, 2 )
        
        # We will detect the height of the terrain by creating a collision
        # ray and casting it downward toward the terrain.  One ray will
        # start above ralph's head, and the other will start above the camera.
        # A ray may hit the terrain, or it may hit a rock or a tree.  If it
        # hits the terrain, we can detect the height.  If it hits anything
        # else, we rule that the move is illegal.
        self.cTrav = CollisionTraverser()

        self.ralphGroundRay = CollisionRay()
        self.ralphGroundRay.setOrigin(0,0,5)
        self.ralphGroundRay.setDirection(0,0,-1)

        self.ralphGroundCol = CollisionNode( 'ralphRay' )
        self.ralphGroundCol.addSolid( self.ralphGroundRay )
        self.ralphGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.ralphGroundCol.setIntoCollideMask(BitMask32.allOff())

        self.ralphGroundColNp = self.ralph.attachNewNode( self.ralphGroundCol )
        self.ralphGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider( self.ralphGroundColNp, self.ralphGroundHandler )

        self.camGroundRay = CollisionRay()
        self.camGroundRay.setOrigin(0,0,1000)
        self.camGroundRay.setDirection(0,0,-1)

        self.camGroundCol = CollisionNode( 'camRay' )
        self.camGroundCol.addSolid( self.camGroundRay )
        self.camGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.camGroundCol.setIntoCollideMask(BitMask32.allOff())

        self.camGroundColNp = base.camera.attachNewNode( self.camGroundCol )
        self.camGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider( self.camGroundColNp, self.camGroundHandler )

        # Uncomment this line to see the collision rays
        self.ralphGroundColNp.show()
        self.camGroundColNp.show()
       
        # Uncomment this line to show a visual representation of the 
        # collisions occuring
        self.cTrav.showCollisions(render)
        
        # Create some lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.3, .3, .3, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(1, 1, 1, 1))
        directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))


    # Records the state of the arrow keys
    def setKey( self, key, value ):
        self.keyMap[ key ] = value


    # Toggles camera (1st person <-> 3rd person)
    def toggleCamera( self ):

        if( self.fpsMode == True ):
            self.fpsMode = False
        else:
            self.fpsMode = True
    

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move( self, task ):

        # save ralph's initial position so that we can restore it,
        # in case he falls off the map or runs into something.
        startpos = self.ralph.getPos()

        if( self.fpsMode == True ):

            # figure out how much the mouse has moved (in pixels)
            md = base.win.getPointer( 0 )
            x = md.getX()
            y = md.getY()
            heading = base.camera.getH()
            pitch   = base.camera.getP()
            if base.win.movePointer( 0, 100, 100 ):
                heading -= ( x - 100 ) * MOUSE_SENSITIVITY
                pitch   -= ( y - 100 ) * MOUSE_SENSITIVITY
            if( pitch < -45 ): pitch = -45
            else:
                if( pitch >  45 ): pitch =  45
            base.camera.setHpr( heading, pitch, 0 )
            self.ralph.setH( base.camera.getH() )

            # If a move key is pressed, move ralph in the specified direction.
            if( self.keyMap["d"] != 0 ):
                self.ralph.setX( self.ralph, STRAFE_SPEED * globalClock.getDt() )
            else:
                if( self.keyMap["a"] != 0 ):
                    self.ralph.setX( self.ralph, -STRAFE_SPEED * globalClock.getDt() )

            if( self.keyMap["w"] != 0 ):
                self.ralph.setY( self.ralph, FORWARD_SPEED * globalClock.getDt() )
            else:
                if( self.keyMap["s"] != 0 ):
                    self.ralph.setY( self.ralph, -BACKWARD_SPEED * globalClock.getDt() )

        else:

            # If a camera rotate key is pressed, move camera in the specified direction.
            base.camera.lookAt(self.ralph)
            if( self.keyMap["d"] != 0 ):
                base.camera.setX( base.camera, -20 * globalClock.getDt() )
            else:
                if( self.keyMap["a"] != 0 ):
                    base.camera.setX( base.camera, +20 * globalClock.getDt() )

            # If a move key is pressed, move ralph in the specified direction.
            if( self.keyMap["w"] != 0 ):
                self.ralph.setH( base.camera.getH() + 180 )
                self.ralph.setY( self.ralph, -FORWARD_SPEED * globalClock.getDt() )
            else:
                if( self.keyMap["s"] != 0 ):
                    self.ralph.setH( base.camera.getH() )
                    self.ralph.setY( self.ralph, -BACKWARD_SPEED * globalClock.getDt() )

            # If ralph is moving, loop the run animation.
            # If he is standing still, stop the animation.
            if( self.keyMap["w"] != 0 ) or ( self.keyMap["s"] != 0 ):
                if self.isMoving is False:
                    self.ralph.loop("run")
                    self.isMoving = True
            else:
                if self.isMoving:
                    self.ralph.stop()
                    self.ralph.pose("walk",5)
                    self.isMoving = False

            # If the camera is too far from ralph, move it closer.
            # If the camera is too close to ralph, move it farther.
            camvec = self.ralph.getPos() - base.camera.getPos()
            camvec.setZ(0)
            camdist = camvec.length()
            camvec.normalize()
            if (camdist > 10.0):
                base.camera.setPos(base.camera.getPos() + camvec*(camdist-10))
            else:
                if (camdist < 7.0):
                    base.camera.setPos(base.camera.getPos() - camvec*(7-camdist))

        # Now check for collisions.
        self.cTrav.traverse(render)

        # Adjust ralph's Z coordinate.  If ralph's ray hit terrain,
        # update his Z. If it hit anything else, or didn't hit anything, put
        # him back where he was last frame.
        entries = []
        for i in range( self.ralphGroundHandler.getNumEntries() ):
            entry = self.ralphGroundHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            self.ralph.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            self.ralph.setPos(startpos)

        if( self.fpsMode == True ):

            base.camera.setPos( self.ralph.getX(), self.ralph.getY(), self.ralph.getZ()+2 )

        else:

            # Keep the camera at one foot above the terrain,
            # or two feet above ralph, whichever is greater.
            entries = []
            for i in range( self.camGroundHandler.getNumEntries() ):
                entry = self.camGroundHandler.getEntry(i)
                entries.append(entry)
            entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                         x.getSurfacePoint(render).getZ()))
            if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
                base.camera.setZ(entries[0].getSurfacePoint(render).getZ()+1.0)
            if (base.camera.getZ() < self.ralph.getZ() + 2.0):
                base.camera.setZ(self.ralph.getZ() + 2.0)

            # The camera should look in ralph's direction,
            # but it should also try to stay horizontal, so look at
            # a floater which hovers above ralph's head.
            self.floater.setPos(self.ralph.getPos())
            self.floater.setZ(self.ralph.getZ() + 2.0)
            base.camera.lookAt(self.floater)

        return task.cont


w = World()
run()

