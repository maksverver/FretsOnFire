#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#####################################################################
# Frets on Fire                                                     #
# Copyright (C) 2006 Sami Kyöstilä                                  #
#                                                                   #
# This program is free software; you can redistribute it and/or     #
# modify it under the terms of the GNU General Public License       #
# as published by the Free Software Foundation; either version 2    #
# of the License, or (at your option) any later version.            #
#                                                                   #
# This program is distributed in the hope that it will be useful,   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of    #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the     #
# GNU General Public License for more details.                      #
#                                                                   #
# You should have received a copy of the GNU General Public License #
# along with this program; if not, write to the Free Software       #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,        #
# MA  02110-1301, USA.                                              #
#####################################################################

"""
Main game executable.
"""

# Register the latin-1 encoding
import codecs
import encodings.iso8859_1
import encodings.utf_8
codecs.register(lambda encoding: encodings.iso8859_1.getregentry())
codecs.register(lambda encoding: encodings.utf_8.getregentry())
assert codecs.lookup("iso-8859-1")
assert codecs.lookup("utf-8")

from GameEngine import GameEngine
from MainMenu import MainMenu
import Log
import Config
import Version

import getopt
import sys
import os

def run():

  while True:
    config = Config.load(Version.appName() + ".ini", setAsDefault = True)
    engine = GameEngine(config)
    engine.setStartupLayer(MainMenu(engine))

    try:
      while engine.run():
        pass
    except KeyboardInterrupt:
        pass
    if engine.restartRequested:
      Log.notice("Restarting.")

      try:
        # Determine whether were running from an exe or not
        if hasattr(sys, "frozen"):
          if os.name == "nt":
            os.execl("FretsOnFire.exe", "FretsOnFire.exe", *sys.argv[1:])
          else:
            os.execl("./FretsOnFire", "./FretsOnFire", *sys.argv[1:])
        else:
          if os.name == "nt":
            bin = "c:/python24/python"
          else:
            bin = "/usr/bin/python"
          os.execl(bin, bin, "FretsOnFire.py", *sys.argv[1:])
      except:
        Log.warn("Restart failed.")
        raise
      break
    else:
      break
  engine.quit()


usage = """%(prog)s [options]
Options:
  --verbose, -v      Verbose messages
  --profile, -p      Generate call profile
""" % {"prog": sys.argv[0] }


if __name__ == "__main__":
  prof = False
  try:
    opts, args = getopt.getopt(sys.argv[1:], "vp", ["verbose","profile"])
  except getopt.GetoptError:
    print usage
    sys.exit(1)

  for opt, arg in opts:
    if opt in ["--verbose", "-v"]:
      Log.quiet = False

    if opt in ["--profile", "-p"]:
      prof = True

  import psyco
  psyco.profile()

  if not prof:
    run()
  else:
    import hotshot, hotshot.stats
    prof = hotshot.Profile("profile")
    prof.runcall(run)
    prof.close()
    stats = hotshot.stats.load("profile")
    stats.strip_dirs()
    stats.sort_stats('cumtime', 'calls')
    stats.print_stats('20')

