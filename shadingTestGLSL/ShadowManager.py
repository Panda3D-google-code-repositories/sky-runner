from pandac.PandaModules import *
import math

def MakeOrthographicCamera( objBuffer, npRoot = None, strCameraName = 'Cam', iCameraMask = None, iSort = 0 ):
	lens = OrthographicLens()
	lens.setFilmSize(1, 1)
	lens.setNearFar(1,50)
	npCam = base.makeCamera( objBuffer, sort = iSort, camName = strCameraName)
	npCam.node().setLens( lens )
	if npRoot:
		npCam.node().setScene( npRoot )
	if iCameraMask:
		npCam.node().setCameraMask( BitMask32(iCameraMask) )
	return npCam

def CreateDepthFBOAndTex( strName = 'Buffer', iSort = -10, iSizeX = None, iSizeY = None ):
	winprops = WindowProperties()
	iSizeX = GetScreenResX() if iSizeX == None else iSizeX
	iSizeY = GetScreenResY() if iSizeY == None else iSizeY
	winprops.setSize( iSizeX , iSizeY )
	fbprops = FrameBufferProperties()
	fbprops.setColorBits(0)
	fbprops.setAlphaBits(0)
	fbprops.setStencilBits(0)
	fbprops.setDepthBits( 1 )
	objBuffer = base.graphicsEngine.makeOutput(base.pipe, strName, iSort, fbprops, winprops, GraphicsPipe.BFCanBindEvery | GraphicsPipe.BFRefuseWindow, base.win.getGsg(), base.win)
	
	objDepthmap = Texture()
	objBuffer.addRenderTexture(objDepthmap, GraphicsOutput.RTMCopyTexture, GraphicsOutput.RTPDepth)
	if (base.win.getGsg().getSupportsShadowFilter()):
		objDepthmap.setMinfilter(Texture.FTShadow)
		objDepthmap.setMagfilter(Texture.FTShadow)
	objDepthmap.setBorderColor(Vec4(1,1,1,1))
	objDepthmap.setWrapU(Texture.WMBorderColor)
	objDepthmap.setWrapV(Texture.WMBorderColor)
	
	return objBuffer, objDepthmap
	
def MakeShadowCamBufferTexture( iSize, iSort, strId = 'Shadow', npRoot = None, iCameraMask = None, booDebugBuffers = False ):
	if booDebugBuffers:
		objBuffer = base.win
		texDepth = None
	else:
		objBuffer, texDepth = CreateDepthFBOAndTex( strName = 'Buffer_' + strId + '_' + str(iSize) + '_' + str(iSort), 
												iSort = iSort, iSizeX = iSize, iSizeY = iSize )
	npCam = MakeOrthographicCamera( objBuffer, npRoot = npRoot, strCameraName = 'Cam_' + strId, iCameraMask = iCameraMask )
	return objBuffer, texDepth, npCam

def PSSMSplit( iSection, intTotalSections, fNear = None, fFar = None, npCam = None):
	#Returns the z-split depth for PSSM for section i, given intTotalSections
	if npCam:
		fNear = npCam.node().getNear()
		fFar = npCam.node().getFar()
	return 0.5*( fNear * ((fFar / fNear) ** (1.*iSection/intTotalSections)) + fNear + (fFar - fNear) * (1.*iSection/intTotalSections) )
	
def GetFrustumBoundsAtDepthZ(fDepth, tupHalfFovRad = None, npCam = None):
	# fHalfHVFovRad =  0.5 * FOV (in radians)   where FOV = (Hor_Fov, Ver_Fov)
	if npCam:
		vb2FovRad = npCam.node().getLens().getFov()
		x = fDepth * math.tan( math.radians( vb2FovRad[0]/2 ) )
		y = fDepth * math.tan( math.radians( vb2FovRad[1]/2 ) )
	else:
		x = fDepth * math.tan( tupHalfFovRad[0] )
		y = fDepth * math.tan( tupHalfFovRad[1] )
	#				ur							ul					ll							lr
	### Remember y+ is forward or Depth
	return Point3( x, fDepth, y), Point3( -x, fDepth, y), Point3( -x, fDepth, -y), Point3( x, fDepth, -y)

class clShadowManager:
	iShadowBufferSortIndexStart = -60
	iShadowCamMaskStart = 64
	booTexelIncrement = True
	def __init__(self, npViewCam, objSpace, tupMapSizes = ( 1024 ), npRoot = None, booTightEncloseEntities = False, vec3LightDir = None, booGhostBuffers = False, booOptimize = True ):
		## vec3LightDir is defined as lightpos - 
		self.booGhostBuffers = booGhostBuffers
		self.booOptimize = booOptimize
		self.booTightEncloseEntities = booTightEncloseEntities
		self.npRoot = npRoot if npRoot else render
		self.npViewCam = npViewCam
		self.objSpace = objSpace
		self.tupMapSizes = tupMapSizes
		self.vec3LightDir = vec3LightDir if vec3LightDir else Vec3( 0, 0, 1)
		
		self.npDebugViewFrustrumBounds = NodePath('0')
		self.npDebugLightDir = None
		
		self.listShadowBuffers = []
		self.listShadowTexs = []
		self.listShadowCams = []
		self.listShadowCams_Debug = []
		
		### Force try a 45 deg shift when constraining the camera
		self.booForceDiagnol = False
		
		### Initiate some constants like split depths in the frustum space
		self.InitViewCamConstants()
		### Create the shadow cams and the buffers
		self.InitShadowBuffTexCam()
		### Orientate the shadow cam correctly
		self.SetAllShadowCamPosFilmSize()

	def ChangeMapSizes(self, tupMapSizes):
		## Reinits the shadow map manager with a new set of tex map sizes
		self.DestroyShadowBufferCamTex()
		self.tupMapSizes = tupMapSizes
		self.InitViewCamConstants()
		self.InitShadowBuffTexCam()
		self.SetAllShadowCamPosFilmSize()

	def ChangeLightDir(self, vec3NewDir):
		self.vec3LightDir = vec3NewDir
		self.SetAllShadowCamPosFilmSize()

	def DebugAutoFrustumRecalc(self):
		taskMgr.add( self.DebugReCalcFrustumTask, 'AutoCalcFrustum' )
		
	def DebugReCalcFrustumTask(self, task):
		self.OnCamMove()
		return task.cont
		
	def DebugDisableAutoReCalcFrustum(self):
		taskMgr.remove( 'AutoCalcFrustum' )
		
	def GetDepthTexture(self, iCam):
		assert( not self.booGhostBuffers )
		return self.listShadowTexs[ iCam ]
		
	def GetLightDir(self):
		return self.vec3LightDir
		
	def GetLightDirAsVB4(self):
		return Vec4( self.vec3LightDir[0], self.vec3LightDir[1], self.vec3LightDir[2], 0 )

	def GetListSplitDepths(self):
		return self.listSplitDepths

	def GetNumberOfShadowCams(self):
		return len(self.listShadowCams)

	def GetNpShadowCam(self, iCam):
		return self.listShadowCams[iCam] 

	def GetTupMapSizes(self):
		return self.tupMapSizes
		
	def InitViewCamConstants(self):
		#### Initializes some invariantes of the views cam such as the split depths, and boundaries of the 
		####  near, far, and split planes. Everything is in the view cam space.
		self.fNear = self.npViewCam.node().getLens().getNear()
		self.fFar = self.npViewCam.node().getLens().getFar()
		## pt3 camera space near _UR...etc.
		## Determine the near far bounds of the View camera...etc.
		self.pt3csNear_UR,  self.pt3csNear_UL, self.pt3csNear_LL, self.pt3csNear_LR = GetFrustumBoundsAtDepthZ( self.fNear, npCam = self.npViewCam )
		self.pt3csFar_UR, self.pt3csFar_UL, self.pt3csFar_LL, self.pt3csFar_LR = GetFrustumBoundsAtDepthZ( self.fFar, npCam = self.npViewCam )
	
		## Determine the split depths and frustumcoords if any
		### fNear fDepth1 fDepth2 fFar
		self.listSplitDepths = [ self.fNear ]
		for i in xrange( len(self.tupMapSizes ) - 1):
			self.listSplitDepths.append( PSSMSplit( iSection = i + 1, intTotalSections = len( self.tupMapSizes ), fNear = self.fNear, fFar = self.fFar ) )
		self.listSplitDepths.append( self.fFar )
		
		self.listSplitPlaneFrustumBounds = [ (self.pt3csNear_UR, self.pt3csNear_UL, self.pt3csNear_LL, self.pt3csNear_LR ) ]
		for i in xrange( len(self.listSplitDepths) -2 ):
			fSplitDepth = self.listSplitDepths[i + 1]
			fUR = (self.pt3csFar_UR - self.pt3csNear_UR)/(self.fFar - self.fNear)*(fSplitDepth - self.fNear)
			fUL = (self.pt3csFar_UL - self.pt3csNear_UL)/(self.fFar - self.fNear)*(fSplitDepth - self.fNear)
			fLL = (self.pt3csFar_LL - self.pt3csNear_LL)/(self.fFar - self.fNear)*(fSplitDepth - self.fNear)
			fLR = (self.pt3csFar_LR - self.pt3csNear_LR)/(self.fFar - self.fNear)*(fSplitDepth - self.fNear)
			self.listSplitPlaneFrustumBounds.append( (fUR, fUL, fLL, fLR) )
		self.listSplitPlaneFrustumBounds.append( ( self.pt3csFar_UR, self.pt3csFar_UL, self.pt3csFar_LL, self.pt3csFar_LR ) )

	def InitShadowBuffTexCam(self):
		self.listShadowBuffers = []
		self.listShadowTexs = []
		self.listShadowCams = []
		self.listShadowCams_Debug = []
		for i in xrange( len( self.tupMapSizes ) ):
			buff, tex, cam = MakeShadowCamBufferTexture( iSize = self.tupMapSizes[i], iSort = self.iShadowBufferSortIndexStart + i, 
					strId = 'Shadow' + str(i), iCameraMask = self.iShadowCamMaskStart*(2**i), npRoot = self.npRoot, booDebugBuffers = self.booGhostBuffers )
			cam.node().setInitialState( RenderState.make(CullFaceAttrib.makeReverse(), ColorWriteAttrib.make(ColorWriteAttrib.COff)) )
			cam.setShaderOff( 999 )
			
			if self.booGhostBuffers:
				cam.node().setActive( 0 )
			else:
				buff.setClearColorActive( False )
				buff.setClearDepthActive( True )
				cam.node().getDisplayRegion(0).setClearColorActive(False)
				
			self.listShadowBuffers.append( buff )
			self.listShadowTexs.append( tex )
			self.listShadowCams.append( cam )
			self.listShadowCams_Debug.append( [] )

	def OnCamMove(self):
		self.SetAllShadowCamPosFilmSize()

	def SetActive(self, booActive):
		for i in self.listShadowCams:
			i.node().setActive( booActive )

	def SetShadowCamPosFilmSize(self, iCam):
		pt3FrustumCenter = self.npRoot.getRelativePoint( self.npViewCam, 
				Point3( 0, 1.*(self.listSplitDepths[iCam] + self.listSplitDepths[iCam+1])/2, 0) )
		## We temporary set the shadow cam above the frustum center in world space
		
		## We use the MSDN sample for snapping texel units to try to reduce shimmering
		## I'm probably doing it incorrectly. oh well!
		fWorldUnitsPerTexel = 1.*(self.listSplitDepths[iCam+1] - self.listSplitDepths[iCam])/self.tupMapSizes[iCam]
		
		npCam = self.listShadowCams[iCam]
		npCam.setPos( pt3FrustumCenter + self.vec3LightDir*(self.listSplitDepths[iCam+1] -self.listSplitDepths[iCam]) )
		npCam.lookAt ( pt3FrustumCenter )
		dNear = 1000
		dFar = -1000
		## We compute two bounding boxes
		## One using the normal z/x axis
		## and the other using a set axis rotated by 45'  We do this instead of computing
		## the convex hull to figure out which camera orientation is the best.
		x_up_min = 1000
		x_up_max = -1000
		z_up_min = 1000
		z_up_max = -1000
		## in world space
		## We take the frustum bounds and convert them into shadow cam space coordinates
		## Then using the transformed pts to find the bounds for the shadow cam and reshift
		## the shadowcam to the center of the bounds.
		## We would do something similiar here if we want to draw even tighter bounds against
		## objects in world space.
		if not self.booOptimize:
			for pt3 in self.listSplitPlaneFrustumBounds[iCam]:
				cspt3 = npCam.getRelativePoint( self.npViewCam, pt3 )
				dNear = min( dNear, cspt3[1] )
				dFar = max( dFar, cspt3[1] )
				x_up_max = max( x_up_max, cspt3[0] )
				x_up_min = min( x_up_min, cspt3[0] )
				z_up_max = max( z_up_max, cspt3[2] )
				z_up_min = min( z_up_min, cspt3[2] )
				
			for pt3 in self.listSplitPlaneFrustumBounds[iCam+1]:
				cspt3 = npCam.getRelativePoint( self.npViewCam, pt3 )
				dNear = min( dNear, cspt3[1] )
				dFar = max( dFar, cspt3[1] )
				x_up_max = max( x_up_max, cspt3[0] )
				x_up_min = min( x_up_min, cspt3[0] )
				z_up_max = max( z_up_max, cspt3[2] )
				z_up_min = min( z_up_min, cspt3[2] )
				
			xOffset = (x_up_max + x_up_min)/2
			zOffset = (z_up_max + z_up_min)/2
			vec2Move = self.npRoot.getRelativeVector( npCam, Vec3( xOffset, 0, zOffset ) )
			npCam.setPos( pt3FrustumCenter + self.vec3LightDir*(self.listSplitDepths[iCam+1] -self.listSplitDepths[iCam]) + vec2Move )
			fFilmWidth = (x_up_max - x_up_min)
			fFilmHeight = (z_up_max - z_up_min )
			if self.booTexelIncrement:
				fFilmWidth = math.floor( fFilmWidth/fWorldUnitsPerTexel )*fWorldUnitsPerTexel
				fFilmHeight = math.floor( fFilmHeight/fWorldUnitsPerTexel )*fWorldUnitsPerTexel
			npCam.node().getLens().setFilmSize( fFilmWidth, fFilmHeight )
			npCam.node().getLens().setNearFar( dNear, dFar )
		else:
			## For the optimize portion we also calculate the bounding box of a rotated coordinate
			## system, rotated by 45 deg to be exact. This is to avoid having to calculate the convex hull
			## and the aligning the square along the longest boundary (as the next possible optimization)
			x_diag_min = 1000
			x_diag_max = -1000
			z_diag_min = 1000
			z_diag_max = -1000
			diag_x = Vec3( 0.707106781, 0, 0.707106781 )
			diag_z = Vec3( -0.707106781, 0, 0.707106781 )
			for pt3 in self.listSplitPlaneFrustumBounds[iCam]:
				cspt3 = npCam.getRelativePoint( self.npViewCam, pt3 )
				dNear = min( dNear, cspt3[1] )
				dFar = max( dFar, cspt3[1] )
				### Calc the bounds 
				x_up_max = max( x_up_max, cspt3[0] )
				x_up_min = min( x_up_min, cspt3[0] )
				z_up_max = max( z_up_max, cspt3[2] )
				z_up_min = min( z_up_min, cspt3[2] )
				
				fDiagXCoord = cspt3.dot( diag_x )
				x_diag_min = min( x_diag_min, fDiagXCoord )
				x_diag_max = max( x_diag_max, fDiagXCoord )
				
				fDiagZCoord = cspt3.dot( diag_z )
				z_diag_min = min( z_diag_min, fDiagZCoord )
				z_diag_max = max( z_diag_max, fDiagZCoord )
				
			for pt3 in self.listSplitPlaneFrustumBounds[iCam+1]:
				cspt3 = npCam.getRelativePoint( self.npViewCam, pt3 )
				dNear = min( dNear, cspt3[1] )
				dFar = max( dFar, cspt3[1] )
				x_up_max = max( x_up_max, cspt3[0] )
				x_up_min = min( x_up_min, cspt3[0] )
				z_up_max = max( z_up_max, cspt3[2] )
				z_up_min = min( z_up_min, cspt3[2] )
				
				fDiagXCoord = cspt3.dot( diag_x )
				x_diag_min = min( x_diag_min, fDiagXCoord )
				x_diag_max = max( x_diag_max, fDiagXCoord )
				
				fDiagZCoord = cspt3.dot( diag_z )
				z_diag_min = min( z_diag_min, fDiagZCoord )
				z_diag_max = max( z_diag_max, fDiagZCoord )
				
			fNormalSize = ( x_up_max - x_up_min ) * ( z_up_max - z_up_min )
			fDiagSize = ( x_diag_max - x_diag_min ) * ( z_diag_max - z_diag_min )
			if (fDiagSize < fNormalSize) | self.booForceDiagnol:
				vecUp = diag_z
				xOffset = (x_diag_max + x_diag_min)/2
				zOffset = (z_diag_max + z_diag_min)/2
				
				fFilmWidth = (x_diag_max - x_diag_min)
				fFilmHeight = (z_diag_max - z_diag_min )
				if self.booTexelIncrement:
					fFilmWidth = math.floor( fFilmWidth/fWorldUnitsPerTexel )*fWorldUnitsPerTexel
					fFilmHeight = math.floor( fFilmHeight/fWorldUnitsPerTexel )*fWorldUnitsPerTexel
					
				vec2Move = self.npRoot.getRelativeVector( npCam, diag_x*xOffset + diag_z*zOffset )
				npCam.setPos( pt3FrustumCenter + self.vec3LightDir*(self.listSplitDepths[iCam+1] -self.listSplitDepths[iCam]) + vec2Move )
				vecUp = self.npRoot.getRelativeVector( npCam, vecUp )
				npCam.lookAt( pt3FrustumCenter + vec2Move, vecUp)
				npCam.node().getLens().setFilmSize( fFilmWidth, fFilmHeight )
			else:
				xOffset = (x_up_max + x_up_min)/2
				zOffset = (z_up_max + z_up_min)/2
				fFilmWidth = (x_up_max - x_up_min)
				fFilmHeight = (z_up_max - z_up_min )
				if self.booTexelIncrement:
					fFilmWidth = math.floor( fFilmWidth/fWorldUnitsPerTexel )*fWorldUnitsPerTexel
					fFilmHeight = math.floor( fFilmHeight/fWorldUnitsPerTexel )*fWorldUnitsPerTexel
					
				vec2Move = self.npRoot.getRelativeVector( npCam, Vec3( xOffset, 0, zOffset ) )
				npCam.node().getLens().setFilmSize( fFilmWidth, fFilmHeight )
				npCam.setPos( pt3FrustumCenter + self.vec3LightDir*(self.listSplitDepths[iCam+1] -self.listSplitDepths[iCam]) + vec2Move )

			npCam.node().getLens().setNearFar( dNear, dFar )

	def SetAllShadowCamPosFilmSize(self):
		for i in xrange(len(self.listShadowCams)):
			self.SetShadowCamPosFilmSize( i )
