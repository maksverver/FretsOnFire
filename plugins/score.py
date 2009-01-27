from plugins import Plugin
import Song
import Data

class new(Plugin):
  def __init__(self):
    self.scores = []
    self.p = -1

  def info(self):
    return { 'author': "Marius van Voorden & Brend Wanders",
             'name':   "Score display++" }
  
  def render(self, scene):
    if not self.scores:
      self.scores = scene.song.info.getHighscores(scene.song.difficulty, 100)
      self.p = len(self.scores)-1

    curscore = scene.player.score + scene.getExtraScoreForCurrentlyPlayedNotes()
    while self.p>=0 and self.scores[self.p][0] < curscore:
      self.p-=1
    
    scale = 0.0009
    
    if self.p==-1:
      self.render_text(scene, "First place!")
    else:
      sw, sh = scene.engine.data.font.getStringSize(unicode(Data.STAR2), scale)
      
      score, stars, name = self.scores[self.p]
      for i in range(stars-1, -1, -1):
        self.render_text(scene, " %s"        %  unicode(Data.STAR2),    scale=scale, increaseLine=False, adjustment=    ((stars-1-i)/2.)*sw+.042)
      self.render_text(  scene, "%d: %s %d " % (self.p+1, name, score), scale=scale,                     adjustment=sw+ ((stars-1  )/2.)*sw+.042)