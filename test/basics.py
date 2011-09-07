from fdl.graph import *

fg = FrameGraph()
fg.config()

w = fg.getWorldFrame()

f=Frame(w,'Tr(x)',name='foo',description='My very first frame')
fg.add(f)

g=Frame(f,'Tr(x)')
fg.add(g)

h=Frame(g,'Tr(x)')
fg.add(h)

z=Frame(f,'Tr(x)')
fg.add(z)

q=Frame(z,'Tr(x)')
fg.add(q)

t=Frame(f,'Tr(x)')
fg.add(t)

print fg.framesbyid
print fg.framesbydep


#assert fg.getCommonBase(w,w)==w

assert fg.getCommonBase(w,f)==w
assert fg.getCommonBase(f,g)==f
assert fg.getCommonBase(f,h)==f
assert fg.getCommonBase(t,g)==f
assert fg.getCommonBase(f,q)==f


fg.add(Variable("foo"))

print fg.variables["foo"]
