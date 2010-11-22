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

def parse(filename):
  parser = Top(
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
		  Att('base',parsebase,lambda c,cc: c[2][cc[1]-1]['id']), # default base is the preceding frame - maybe XML + XPath wasn't such a bad idea after all
		  Att('matrix')
	  ),
  )

  tree=yaml.load(file(filename,'r'))
  parser.parse(tree)
  return tree

#c[1][cc[1]]['id']
