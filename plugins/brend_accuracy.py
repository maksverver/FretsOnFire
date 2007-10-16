from plugins import Plugin
import Song
import Theme
import Data

class new(Plugin):
  def info(self):
    return { 'author': "Brend Wanders",
             'name':   "Accuracy display" }

  def render(self, scene):
    if not scene.song:
      return

    song   = scene.song
    guitar = scene.guitar
    font   = scene.engine.data.font

    w, h = font.getStringSize(" ")
    y = .05 - h / 2
    scale = 0.0013 
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

    Theme.setSelectedColor();
    stars = int(5.0 * (accuracy + 0.05))
    msg = "%.2f%% %s" % (100.0*accuracy,unicode(Data.STAR2 * stars + Data.STAR1 * (5 - stars)))
    tw, th = font.getStringSize(msg,scale)
    font.render(msg, (1-tw-th, y + 2*h), scale = scale)

