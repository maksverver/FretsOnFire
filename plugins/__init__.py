from dircache import listdir
import sys

# The plugin base class
class Plugin:
  'Abstract base class for plug-ins'

  def render(self, scene):
    '''Called with a GuitarScene argument while playing.'''
    pass

  def info(self):
    '''Returns a dict containing information about the plug-in.
Recognized keys are:
 name:   Name of the plug-in
 author: Name of the author(s) of the plug-in'''
    return {}

def load():
  plugins = []
  sys.path = ['plugins'] + sys.path
  for file in listdir('plugins'):
    if file[-3:] == '.py' and file[:-3] <> '__init__':
      mod = file[:-3]
      try:
        m = __import__(mod)
        plugins.append(m.new())
      except Exception, e:
        print e
      except:
        print 'Could not load module %s!' % mod
  sys.path = sys.path[1:]
  return plugins
