import types
import yaml
from yap.structparser import *


def parsebase(x,c,cc):
  if x == 'world':
    return 0
  try:
    return int(x)
  except:
    for d in c[2]:
      if 'name' in d:
        if d['name'] == x:
          return d['id']

  raise Exception("No suitable base found. What is %s?" % x)
    

def parseframeid(x,c,cc):
  y=int(x)
  if y==0:
    raise Exception("Sorry, but 0 is reserved as id for the world frame")
  return y

def defaulterbase(c,cc):
  if cc[1]==0:
    return 0
  return c[2][cc[1]-1]['id'] # default base is the preceding frame - maybe XML + XPath wasn't such a bad idea after all

fdlParser = Top(
	  List('variables',
		  Att('name'),
		  Att('deriv',lambda x,c,cc : x.split(),lambda c,cc: ['d' + c[0]['name'],'dd' + c[0]['name'] ]),
		  Att('type',None,'linear'),
		  Att('bounds',lambda x,c,cc : x.split())
	  ),
	  List('frames',
		  Att('id',parseframeid),
		  Att('name',None,lambda c,cc: str(c[0]['id'])),
		  Att('description',None,lambda c,cc: 'Frame {%d}' % c[0]['id']),
		  Att('base',parsebase,defaulterbase), 
		  Att('matrix')
	  ),
  )

def parse(filename,debug=False):
  if isinstance(filename,file):
    tree=yaml.load(filename)
  else:
    tree=yaml.load(file(filename,'r'))
  fdlParser.parse(tree,debug)
  return tree

class fdl:
  """
    Fdl helper class.

    Example usage:
    from fdl.parser import fdl
   
    f = fdl('myfile.fdl')
    f.tree # gives you the whole structure
    f.getFrame(number|name) # gives you a certain frame
    f.getVariable(name) # gives you a certain variable

  """
  def __init__(self,filename,debug=False):
    self.tree=parse(filename,debug)

  def getFrame(self,nameorid):
    if isinstance(nameorid,int):
      myid=nameorid
      for f in self.tree['frames']:
        if f['id'] == myid:
          return f
    else:
      myname=nameorid
      for f in self.tree['frames']:
        if f['name'] == myname:
          return f
    raise Exception("Did not find frame with name %s in %s" % (name,self.tree))


  def getVariable(self,name):
    for f in self.tree['variables']:
      if f['name'] == name:
        return f
    raise Exception("Did not find variable with name %s in %s" % (name,self.tree))

  def getFrames(self):
    return self.tree['frames']


  def addFrame(self,framestruct):
    self.tree['frames'].append(framestruct)
    self.tree=fdlParser.parse(fdlParser)
