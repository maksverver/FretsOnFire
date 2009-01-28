from plugins import Plugin
import Song
import Theme
import Data

class new(Plugin):
  def __init__(self):
    self.scores = []
    self.p = -1

  def info(self):
    return { 'author': "Brend Wanders",
             'name':   "Score display" }
  
  def render_text(self,scene,msg):
    font = scene.engine.data.font

    scale = 0.0013
    tw,th = font.getStringSize(msg,scale)
    w,h = font.getStringSize(msg)
    y = .05 - h / 2

    Theme.setSelectedColor()
    font.render(msg,(1-tw-th,y+3*h),scale=scale)

  def render(self, scene):
    if not scene.song:
      return

    if not self.scores or scene.countdown > 0:
      self.scores = scene.song.info.getHighscores(scene.song.difficulty,100)
      self.p = len(self.scores)-1

    curscore = scene.player.score + scene.getExtraScoreForCurrentlyPlayedNotes()
    while self.p>=0 and self.scores[self.p][0] < curscore:
      self.p-=1
    
    if self.p==-1:
      self.render_text(scene,"First place!")
    else:
      score,stars,name = self.scores[self.p]
      self.render_text(scene,"%d: %s %d" % (self.p+1,name,score))

