import types
from fdl.parser import fdl

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
    print "init Frame", base
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

  def config(self,filename,frameClass=None,worldframeClass=None,debug=False):
    """
    optional keyword attribute frameClass allows you to specify a class inheriting from Frame
    """
    if worldframeClass is None:
      worldframeClass=WorldFrame
    self.world = worldframeClass(self)
    self.framesbyid = {0:self.world}
    self.framesbyname = {'world':self.world}
    self.framesbydep = dict()
    if self.isconfigured:
      raise Exception("FrameGraph is already configured\n")
    self.fdl=fdl(filename,debug)
    if frameClass is None:
      frameClass=Frame

      
    
    print "Initializing with", frameClass
    for frame in self.fdl.getFrames():
      self.add(frameClass(self.getFrame(frame['base']),frame['matrix'],name=frame['name'],description=frame['description'],id=frame['id']))
    self.isconfigured = True

  def getAvailableId(self):
    return len(self.framesbyid)

