from dircache import listdir
import sys
import Log
import Theme
import Config
import plugins
from Resource import Resource
import Version
from OpenGL.GL import *
from Language import _
from Settings import ConfigChoice

class Alignment:
  LEFT  =(0, lambda w,a: a)
  RIGHT =(1, lambda w,a: 1-w-a)
  CENTER=(2, lambda w,a: 0.5-(w/2.0)+a)
  COUNT = 3

# The plugin base class
class Plugin:
  'Abstract base class for plug-ins'
  rules = [0.152 for _ in range(Alignment.COUNT)]

  def __init__(self):
    if hasattr(self, "settings"):
      #self.settings is an array of tuples: (setting name, setting type, default value, setting text, dict or list of possible values)
      for s in self.settings:
        Config.define("plugins", "plugin_" + str(self.__class__) + "." + s[0], s[1], default = s[2], text = _(s[3]), options = s[4])
    
  def render(self, scene):
    '''Called with a GuitarScene argument while playing.'''
    pass

  def info(self):
    '''Returns a dict containing information about the plug-in.
Recognized keys are:
 name:         Name of the plug-in
 author:       Name of the author(s) of the plug-in'''
    return {}
    
  def getConfigChoices(self, config):
    if hasattr(self, "settings"):
      return [
        ConfigChoice(config, "plugins", "plugin_" + str(self.__class__) + "." + s[0], autoApply = True) for s in self.settings
      ]

  #Gets the setting you requested. Saves typing
  def getSetting(self, scene, option):
    return scene.engine.config.get("plugins", "plugin_" + str(self.__class__) + "." + option)
  
  def render_text(self, scene , msg, alignment=Alignment.RIGHT, adjustment=0.042, scale=0.0013, 
                  y=-1, spacing=0.002, increaseLine=True, color=None, alpha=1, direction = (1,0,0)):
    font = scene.engine.data.font  
    
    #Allows for delivering the adjustment as a message of which the width will be taken
    if type(adjustment) is unicode:
      if not direction == (1,0,0):
        adjustment,_ = font.getStringSizeDir(adjustment, scale, direction)
      else:
        adjustment,_ = font.getStringSize(adjustment, scale)
        
    if not direction == (1,0,0):
      w,h = font.getStringSizeDir(msg, scale, direction)
    else:
      w,h = font.getStringSize(msg, scale)
    
    #If no height is given, pick a height beneath the last line
    if y == -1:
      if increaseLine:
        y = self.getFreeY(alignment, h + spacing)
      else:
        y = self.getFreeY(alignment, 0)
      y += spacing
    
    #If the text is beneath the screen, put the text at the bottom
    if y + h > 0.75:
      y = 0.75 - h
  
    if not color:
      Theme.setSelectedColor(alpha)
    else:
      glColor4f(*(color + (alpha,)))
      
    x = alignment[1](w,adjustment)
    font.render(msg, (x, y), scale=scale, direction=direction)
  
  #Returns a height which is free at the side specified
  #Increases the free height with the specified adjustment
  @classmethod
  def getFreeY(self, alignment, increase=0):
    a,_ = alignment
    Plugin.rules[a] += increase
    return Plugin.rules[a] - increase

def onFrame():
  Plugin.rules = [0.152 for _ in range(Alignment.COUNT)]

def load(config):
  plugins = []
  sys.path = ['plugins'] + sys.path
  for file in listdir('plugins'):
    if file[-3:] == '.py' and file[:-3] <> '__init__':
      mod = file[:-3]
      #try:
      m = __import__(mod)
      plugins.append(m.new())
      #except Exception, e:
      #  print e
      #  Log.error("Could not load module %s!" % mod)
      #  Log.error(e)
      #except:
      #  Log.error('Could not load module %s!' % mod)
  sys.path = sys.path[1:]
  
  plugdict = dict([(n, n+1) for n in range(-1,len(plugins))])
  plugdict[-1] = 'Off'
  
  for p in plugins:
    Config.define("plugins", "plugin_" + str(p.__class__), int, len(plugins), text = p.info().get('name'), options = plugdict)
    
  def getOrder(config, p):
    return config.get("plugins", "plugin_" + str(p.__class__))
 
  #Selectionsort
  for i in range(0,len(plugins)):
    a = i
    b = len(plugins)+1
    for j in range(i,len(plugins)):
    
      order = getOrder(config, plugins[j])
      
      if order != -1 and order < b:
        b = order
        a = j
    tmp = plugins[a]
    plugins[a] = plugins[i]
    plugins[i] = tmp
    
    if getOrder(config, plugins[i]) != -1:
      config.set("plugins", "plugin_" + str(plugins[i].__class__), i)
  
  return plugins