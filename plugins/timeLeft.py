from plugins import Plugin
import Song
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

    left = int((self.endtime - song.getPosition()) / 1000.0 + 0.9)

    if left > 0:
      secleft = left % 60
      minleft = left / 60
      msg = "%d:%02d" % (minleft,secleft)
    else:
      msg = "Done"
      
    self.render_text(scene, msg, scale=0.0009)

