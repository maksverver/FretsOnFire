from plugins import Plugin
import Song
import Data
import Config
from Language import _

class new(Plugin):
  def __init__(self):
    self.font = None
    self.settings = [
      ("mode", int, 0, "Display mode", {-1: _("% Only"), 0: _("Bar"), 1: _("Stars")}),
      ("circles", int, 30, "Number of circles in bar", dict([(n, n) for n in range(1, 100)]))
    ]
    
    Plugin.__init__(self)
  
  def info(self):
    return { 'author':      "Brend Wanders & Marius van Voorden",
             'name':        "Accuracy display" }
             
  def render(self, scene):
    song   = scene.song
    guitar = scene.guitar

    t = max([ song.getPosition() - 2*guitar.lateMargin ] + [time for time,event in song.track.getAllEvents() if isinstance(event, Song.Note) and event.played])
    played = missed = 0
    for time,event in song.track.getAllEvents():
      if isinstance(event, Song.Note) and time <= t:
        if event.played:
          played += 1
        else:
          missed += 1
    if played + missed == 0:
      accuracy = 1.0
    else:
      accuracy = (1.0*played)/(played + missed)
      
    mode = self.getSetting(scene, "mode")
    
    if mode == 0:
      if self.font == None:
        self.scale = 0.0013
        self.font = scene.engine.data.font
        self.bw,_ = self.font.getStringSize(unicode(Data.BALL1), scale=self.scale)
        self.sbw,_ = self.font.getStringSizeDir(unicode(Data.BALL1 * 2), direction = (0.08, 0, 0), scale=self.scale)
        self.sbw -= self.bw
        self.dir = (-0.08, 0, 0)
        self.n = self.getSetting(scene, "circles")
      
      if accuracy != 1:
        red = "%s" % unicode(Data.BALL1 * int(self.n*(1-accuracy)))
        adj1,_ = self.font.getStringSizeDir(red, direction = self.dir, scale=self.scale)
        adj1 = -1 * adj1 + self.bw
        self.render_text(scene, red, direction = self.dir, adjustment = adj1+0.042, color=(1,0,0), alpha = 1, increaseLine=False)
        adj1 += self.sbw
      else:
        adj1 = 0
      
      if accuracy != 0:
        green = "%s" % unicode(Data.BALL1 * (self.n-int(self.n*(1-accuracy))))
        adj2,_ = self.font.getStringSizeDir(green, direction = self.dir, scale=self.scale)
        adj2 = -1 * adj2 + self.bw
        self.render_text(scene, green, direction = self.dir, adjustment = adj1+adj2+0.042, color=(0,1,0), alpha = 1, increaseLine=False)
        adj2 += self.sbw
      else:
        adj2 = 0
      
      self.render_text(scene, "%.2f%% " % (100*accuracy), adjustment=adj1+adj2+self.bw+0.042)
      
      #acc = int(100*accuracy)
      #self.render_text(scene, " %s" % unicode(Data.BALL1 * int(n*accuracy)),   direction = (-0.05, 0, 0), adjustment = 2*(adj+bw)+0.042, color=(0,1,0), increaseLine=False)
      #adj,_ = scene.engine.data.font.getStringSizeDir("%s" % unicode(Data.BALL1 * n), scale, direction = (-0.05, 0, 0))
      #self.render_text(scene, "%.2f%% " % (100*accuracy), adjustment=-1*adj+0.42+bw)
      
      
      #self.render_text(scene, msg, direction = (-0.05, 0, 0), adjustment = adj+bw+0.042)
      
      #msg = "%.2f%% %s" % (100*accuracy, unicode(Data.BALL1 * int((n-n*acc/100.)) + Data.BALL1 * int((n*acc/100.))))
      #self.render_text(scene, msg, direction = (-0.05, 0, 0), adjustment = -1*adj+0.042+bw)
      
      
#      for i in range(n):
 #       if i >= (n-acc/100.*n):
  #        self.render_text(scene, " %s" % unicode(Data.BALL1), increaseLine=False, color=(0,1,0), alpha = 0.3, spacing=0.005, adjustment= ((i)/(5.*n/20))*bw+.042)
   #     else:
    #      self.render_text(scene, " %s" % unicode(Data.BALL1), increaseLine=False, color=(1,0,0), alpha = 0.3, spacing=0.005, adjustment= ((i)/(5.*n/20))*bw+.042)
     # self.render_text(  scene, "%.2f%% " % (100*accuracy), adjustment=bw+((n-1)/(5.*n/20))*bw+.042)
      
    elif mode == 1:
      stars = int(5.0 * (accuracy + 0.05))
      msg = "%.2f%% %s" % (100*accuracy, unicode(Data.STAR2 * stars + Data.STAR1 * (5-stars)))
      self.render_text(scene, msg)
      
    else:
      msg = "%.2f%%" % (100*accuracy)
      self.render_text(scene, msg)
    
