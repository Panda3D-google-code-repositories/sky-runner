
import sys
import direct.ffi.panda3d
import panda3d

mod = 'bullet'
lib = 'libpandabullet'

module = direct.ffi.panda3d.panda3d_submodule(mod, lib)
sys.modules["panda3d." + mod] = module
panda3d.bullet = module

