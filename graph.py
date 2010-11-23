import types
from fdl.parser import fdl

class Frame:
  def __init__(self,base,matrix,name='',description='',id=None):
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
  def __init__(self,fg):
    self.fg=fg
  pass


class FrameGraph:
  isconfigured = False
  def __init__(self,filename=None):

    if not(filename is None):
      self.config(filename)

  def add(self,object):
    if isinstance(object,Frame):
      self.framesbyid[object.id] = object
      self.framesbyname[object.name] = object
      self.framesbydep[self.getFrame(object.base)] = object
    else:
      raise Exception("FrameGraph's add method is expecting a Frame object")
  def getWorldFrame(self):
    return self.getFrame(0)

  def getFrame(self,keyword):
    if isinstance(keyword,int):
      return self.framesbyid[keyword]
    if isinstance(keyword,types.StringType):
      return self.framesbyname[keyword]
    if isinstance(keyword,Frame):
      return keyword

  def config(self,filename,frameClass=None,worldframeClass=None):
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
    self.fdl=fdl(filename)
    if frameClass is None:
      frameClass=Frame

      
    
    print "Initializing with", frameClass
    for frame in self.fdl.getFrames():
      self.add(frameClass(self.getFrame(frame['base']),frame['matrix'],name=frame['name'],description=frame['description'],id=frame['id']))
    self.isconfigured = True

  def getAvailableId(self):
    return len(self.framesbyid)

