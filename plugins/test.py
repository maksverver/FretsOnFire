from plugins import Plugin
from plugins import Alignment

class new(Plugin):

  def __init__(self):
    Plugin.__init__(self)
    self.data = []
    self.cnt = 0

  def info(self):
    return { 'author': "Maks Verver",
             'name':   "Test"}
  
  def render(self, scene):
    self.cnt += 1
    text = "%d"  % self.cnt
    self.render_text(scene, text, scale=0.01, adjustment=0, alignment=Alignment.CENTER, color=(1,0.5,0.7), alpha=0.5)
