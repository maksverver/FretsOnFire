from plugins import Plugin
import Song
import Theme
import Data

class new(Plugin):
  def __init__(self):
    self.endtime = 0
    
  def info(self):
    return { 'author': "Brend Wanders",
             'name':   "Time display" }

  def render(self, scene):
    song   = scene.song
    if not self.endtime:
     self.endtime = max([time+event.length for time,event in song.track.getAllEvents() if isinstance(event, Song.Note)])

    font   = scene.engine.data.font

    Theme.setSelectedColor();
    left = int((self.endtime - song.getPosition()) / 1000.0 + 0.9)

    if left > 0:
      secleft = left % 60
      minleft = left / 60
      msg = "%d:%02d" % (minleft,secleft)
    else:
      msg = "Done"
    
    scale = 0.0013
    w,h = font.getStringSize(msg)
    tw, th = font.getStringSize(msg,scale)
    y = .05 - h / 2
    font.render(msg, (1-tw-th, y + 4*h), scale = scale)

