import types
from fdl.parser import fdl
from numpy import pi

import ipdb

class Frame:
  """
   A class that represents a frame
   
   Has attributes: 
     - base Frame
     - name String
     - matrix
     - description String
     - id
     
  The above are suggestions only, this class really doesn't care about the types of the attributes
  
  
  """
  def __init__(self,base,matrix,name='',description='',id=None):
    """
     Construct a Frame.
     
     If no id is supplied, the first available id is used (supplied by FrameGraph)
     
    """
    #print "init Frame", base
    self.fg = base.fg
    self.base = base
    self.name = name
    self.matrix = matrix
    self.description = description
    if id is None:
      self.id = self.fg.getAvailableId()
    else:
      try:
        self.id = int(id)
      except:
        self.id = id
        
class WorldFrame(Frame):
  """
   A subclass of Frame to denote the World Frame
  """
  def __init__(self,fg):
    self.fg=fg
    self.name="world"
    self.description="Inertial world frame"
    self.id=0
  pass

class Variable:
  def __init__(self,name="foo",deriv=None,type="linear",bounds=None,default=None):

    if deriv==None:
      deriv = ['d'+name,'dd'+name]
    cand = ["linear","angular","real"]
    if not(type in cand):
      raise Exception("Unknown variable type %s. Pick one of %s" % (type,str(cand)))
    
    if type=='linear' or "type"=='real':
      bounds = [-10.0,10.0]
    elif type=='angular':
      bounds = [-pi,pi]

    if default==None:
      default = (bounds[0] + bounds[1])/2.0
      
    self.name    = name
    self.type    = type
    self.deriv   = deriv
    self.bounds  = bounds
    self.default = default
    
  def __str__(self):
    fields = ["name","deriv","type","bounds", "default"]
    s = []
    for f in fields:
      s.append("%s=%s" % (f,str(getattr(self,f))))
    
    return "Variable(" + ", ".join(s) + ")"


class FrameGraph:
  """
  A class that represents a graph of Frames
  """
  isconfigured = False
  def __init__(self,filename=None,debug=False):

    if not(filename is None):
      self.config(filename,debug=debug)

  def add(self,object):
    """
    
     Expecting one of:
      - Frame
      
    
    """
    if isinstance(object,Frame):
      self.framesbyid[object.id] = object
      self.framesbyname[object.name] = object
      if self.getFrame(object.base) in self.framesbydep:
        self.framesbydep[self.getFrame(object.base)].append(object)
      else:
        self.framesbydep[self.getFrame(object.base)] = [object]
      self.frames.append(object)
      return object
    elif isinstance(object,Variable):
      self.variable[object.name] = object
      self.variables.append(object)
      return object
    else:
      raise Exception("FrameGraph's add method is expecting a Frame object")
      
  def getWorldFrame(self):
    """
     Return the World Frame
    """
    return self.getFrame(0)

  def getFrame(self,keyword):
    """
      keyword can be integer, string, frame (in which case you get the argument back)
    """
    if isinstance(keyword,int):
      return self.framesbyid[keyword]
    if isinstance(keyword,types.StringType):
      return self.framesbyname[keyword]
    if isinstance(keyword,Frame):
      return keyword

  def config(self,filename=None,frameClass=None,worldframeClass=None,debug=False):
    """
    
    config()
      just start with a WorldFrame
      
    config(filename)
      start from an fdl file
    
    optional keyword attribute frameClass allows you to specify a class inheriting from Frame
    """
    if worldframeClass is None:
      worldframeClass=WorldFrame
    if frameClass is None:
      frameClass=Frame
    #print "Initializing with", frameClass
    self.world = worldframeClass(self)
    self.framesbyid = {0:self.world}
    self.framesbyname = {'world':self.world}
    self.framesbydep = dict()
    self.frames = [self.world]
    self.variable = dict()
    self.variables = []
    if self.isconfigured:
      raise Exception("FrameGraph is already configured\n")
      
    if isinstance(filename,FrameGraph):
      fg = filename
      for frame in fg.frames:
        if not(isinstance(frame,WorldFrame)):
          self.add(frameClass(self.getFrame(frame.base.id),frame.matrix,name=frame.name,description=frame.description,id=frame.id))
      for v in fg.variables:
        self.add(Variable(v.name,deriv=v.deriv,type=v.type,bounds=v.bounds,default=v.default))
    elif not(filename is None):
      self.fdl=fdl(filename,debug)
      for frame in self.fdl.getFrames():
        self.add(frameClass(self.getFrame(frame['base']),frame['matrix'],name=frame['name'],description=frame['description'],id=frame['id']))
      for v in self.fdl.getVariables():
        self.add(Variable(v["name"],deriv=v["deriv"],type=v["type"],bounds=v["bounds"],default=v["default"]))
      
    self.isconfigured = True

  def getAvailableId(self):
    """
    
    Return a frame identifier that is unoccupied
    
    """
    return len(self.framesbyid)
    
    
  
  def getHierarchy(self,frame):
    """
    return a list of the node id itself and the ids of all its ancenstors.
    """
    f = self.getFrame(frame)
    if hasattr(f,'base'):
      return [f] + self.getHierarchy(f.base)
    else:
      return [f]
    
  def getCommonBase(self,id1,id2):
    """
    Given two frames, find the common base frame
    """
    h1 = self.getHierarchy(id1)
    h1.reverse()
    h2 = self.getHierarchy(id2)
    h2.reverse()
        
    common = None
    for i in range(0,min(len(h1),len(h2))):
      if h1[i]==h2[i]:
        common = h1[i]
        
    return common 

