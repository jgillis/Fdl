from fdl.graph import *

fg = FrameGraph()
fg.config()

w = fg.getWorldFrame()

f=Frame(w,'Tr(x)',name='foo',description='My very first frame')

fg.add(f)

print f.framesbyid
print f.framesbydep
