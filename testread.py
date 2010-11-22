from fdl.parser import fdl,parse
from fdl.graph import *

print parse('sample.fdl')

f=fdl('sample.fdl')

print f.getFrame(1)

print f.getVariable('theta')

fg = FrameGraph('sample.fdl')




