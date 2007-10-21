from plugins import Plugin
from time import time

interval = 1	# measurement interval in seconds

class new(Plugin):

  def __init__(self):
    Plugin.__init__(self)
    self.data = []

  def info(self):
    return { 'author': "Maks Verver",
             'name':   "Display frames-per-second" }
  
  def render(self, scene):
    if scene.song:
      now = float(time())
      self.data.append(now)
      p = 0
      while self.data[p] < now - interval:
        p += 1
      self.data = self.data[p:]
      if len(self.data) > 1:
        text = "%.2f fps"  % ((len(self.data) - 1)/(now - self.data[0]))
        font = scene.engine.data.font
        scale = 0.001
        w,h = font.getStringSize(text, scale)
        font.render(text, (1 - w, .75 - h), scale=scale)
