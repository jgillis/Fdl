from fdl.parser import fdl,parse


print parse('sample.fdl')

f=fdl('sample.fdl')

print f.getFrame(1)

print f.getVariable('theta')
