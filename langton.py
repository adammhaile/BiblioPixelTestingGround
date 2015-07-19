import time
from bibliopixel.animation import *
from bibliopixel import *

import random

#animation class
class LangtonsAnt(BaseMatrixAnim):
    def __init__(self, led, antColor=colors.Green, pathColor=colors.Red):
        super(LangtonsAnt, self).__init__(led)
        self.antColor = antColor
        self.pathColor = pathColor
        self.offColor = colors.Off
        self.curColor = self.offColor
        self.x = random.randrange(self.width)
        self.y = random.randrange(self.height)
        self.d = random.randrange(4)

    def __rollValue(self, val, step, min, max):
    	val += step
    	if val < min:
    		diff = min-val
    		val = max-diff+1
    	elif val > max:
    		diff = val - max
    		val = min + diff - 1
    	return val

    def __changeDir(self, dir):
    	if dir: dir = 1
    	else: dir = -1
    	self.d = self.__rollValue(self.d, dir, 0, 3)

    def __moveAnt(self):
    	if self.d == 0:
    		self.y = self.__rollValue(self.y, 1, 0, self.height-1)
    	elif self.d == 1:
    		self.x = self.__rollValue(self.x, 1, 0, self.width-1)
    	elif self.d == 2:
    		self.y = self.__rollValue(self.y, -1, 0, self.height-1)
    	elif self.d == 3:
    		self.x = self.__rollValue(self.x, -1, 0, self.width-1)

    	self.curColor = self._led.get(self.x, self.y)
    	self._led.set(self.x, self.y, self.antColor)


    def step(self, amt=1):
        if self.curColor == self.pathColor:
        	self._led.set(self.x, self.y, self.offColor)
        	self.__changeDir(False)
        	self.__moveAnt()
        else:
        	self._led.set(self.x, self.y, self.pathColor)
        	self.__changeDir(True)
        	self.__moveAnt()
