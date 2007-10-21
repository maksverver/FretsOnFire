import asyncore, socket
from urllib import urlopen, quote
from time import time
import Cerealizer
from Log import warn,notice

DELAY=180
cache = { }

class HTTPGet(asyncore.dispatcher):

    def __init__(self, host, path):
        asyncore.dispatcher.__init__(self)
        self.buffer = '\r\n'.join([
            'GET %s HTTP/1.0' % path,
            'Host: %s' % host ]) + '\r\n\r\n'
        self.response = ""
        self.startTime = time()
        self.endTime   = None
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, 80))

    def handle_connect(self):
        pass

    def handle_close(self):
        self.endTime = time()
        self.close()

    def handle_read(self):
        self.response += self.recv(8192)

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def done(self):
        return self.endTime or self.startTime < time() - 30   # 30 sec time-out

    def getResponseBody(self):
        try:
            return self.response[self.response.find("\r\n\r\n") + 4:]
        except ValueError:
            return None

def fetchScores(song, difficulty):
    global cache
    asyncore.loop(0.001, False, None, 1)
    request, scores = cache.get(song, (None, {}))

    if request and request.done() and request.response:
        try:
            newScores = {}
            data = Cerealizer.loads(request.getResponseBody())
            for entry in data:
                diff = entry['difficulty']
                if diff not in newScores:
                    newScores[diff] = []
                newScores[diff].append((entry['score'], entry['stars'], entry['player']))
            scores = newScores
        except:
            warn("Could not parse scores for song %s!" % song)
        request.response = None
    if not request or request.startTime < time() - DELAY:
        notice("(Re)fetching for %s..." % song)
        try:
          request = HTTPGet('hell.student.utwente.nl', '/fretsonfire/scores/?song=%s' % quote(song))
        except:
          warn("Webscore module could not connect to server!")
    cache[song] = request, scores
    return scores.get(difficulty, [])
