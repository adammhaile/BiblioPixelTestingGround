import libavg
from libavg import app, geom, player

import time
import threading

import os, sys

from bibliopixel import *

from bibliopixel.drivers.network_receiver import ThreadedDataServer, ThreadedDataHandler

class VectorDiv(app.MainDiv):
    def onInit(self, updateFunc):
        self._pixels = []
        self.w = 32
        self.h = 32
        self.pixelSize = 10

        self.initGrid()

        self._hasFrame = False

        self.data = [0]*self.w*self.h*3

        address = ('localhost', 1618)
        try:
            server = ThreadedDataServer(address, ThreadedDataHandler)
            server.update = updateFunc
            #server.hasFrame = self.hasFrame

            t = threading.Thread(target=server.serve_forever)
            t.setDaemon(True) # don't hang on exit
            t.start()#
        except Exception as e:
            log.logger.exception(e)
            log.logger.error("Unable to open port. Another visualizer is likely running. Exiting...")
            sys.exit(2)

    def toHexColor(self, r,g,b):
        return "{0:02x}{1:02x}{2:02x}".format(r,g,b)

    def onFrame(self):
    	try:
	        data = self.data
	        for x in range(self.w):
	            for y in range(self.h):
	                i = x+(y*self.w)
	                r = data[i * 3 + 0]
	                g = data[i * 3 + 1]
	                b = data[i * 3 + 2]

	                p = self._pixels[i]
	                p.fillcolor = self.toHexColor(r,g,b)
	        # pass
        except Exception, e:
        	print "onFrame Error"
        	print e

    def initGrid(self):
        pw = self.pixelSize
        ph = pw
        for x in range(self.w):
            for y in range(self.h):
                n = libavg.RectNode(pos=(x*pw,y*ph), color="666666", fillopacity=1, 
                    fillcolor="000000", size=(pw,ph), parent=self)
                self._pixels.append(n)


    def __updatePixels(self, data):
    	try:
        	self.data = data
        except Exception, e:
    		print "__updatePixels error"
    		print e

    # def hasFrame(self):
    # 	return self._hasFrame

def updatePixels(d, data):
        try:
            player.callFromThread(lambda: d.__updatePixels(data))
        except Exception, e:
            print "update error"
            print e

div = VectorDiv(updatePixels)

app.App().run(div, app_resolution='500x500')


