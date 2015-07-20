import bibliopixel.colors as colors
from bibliopixel.animation import BaseGameAnim
import math
from random import randint

class Snake(BaseGameAnim):
    def __init__(self, led, inputDev):
        super(Snake, self).__init__(led, inputDev)
        self._speed = 0.5
        self._lastKeys = None
        self._apple = (-1, -1)
        self._gameOver = False
        self._gameOverCount = 0
        self.resetBody()
        self.placeApple()

    def drawBody(self):
        for b in self._body:
            x,y = b
            self._led.set(x, y, colors.Red)

    def resetBody(self):
        self._pos = (self._led.width/2,self._led.height/2)
        self._body = [self._pos, (self._pos[0], self._pos[1]+1)]
        self._dir = (0, -1)

    def gameOver(self):
        self._gameOver = True
        self._gameOverCount = 0

    def move(self):
        d = tuple(x * y for x,y in zip(self._dir, (self._speed, self._speed)))
        self._pos = tuple(x + y for x,y in zip(d, self._pos))
        if self._pos[0] % 1 == 0 and self._pos[1] % 1 == 0:
            x,y = self._pos
            x,y = (int(x),int(y))
            self._body.insert(0, (x,y))
            if (x,y) != self._apple:
                del self._body[-1]
                if(x < 0 or x >= self.width or y < 0 or y >= self.height):
                    self.gameOver()
            else:
                self.placeApple()

    def placeApple(self):
        x = randint(0, self.width-1)
        y = randint(0, self.height-1)
        self._apple = (x, y)

    def drawApple(self):
        x,y = self._apple
        self._led.set(x, y, colors.Green)

    def step(self, amt=1):
        if not self._gameOver:
            if self._keys != self._lastKeys:
                self._pos = self._body[0]
                if self._keys.UP:
                    self._dir = (0,-1)
                if self._keys.DOWN:
                    self._dir = (0,1)
                if self._keys.RIGHT:
                    self._dir = (1,0)
                if self._keys.LEFT:
                    self._dir = (-1,0)

            self._lastKeys = self._keys

            self.move()
            self._led.all_off()
            self.drawBody()
            self.drawApple()
        else:
            self._led.all_off()
            self._led.drawText("GAME", self.width/2-11, self.height/2-8)
            self._led.drawText("OVER", self.width/2-11, self.height/2+1)
            self._gameOverCount += 1
            if self._gameOverCount > 45:
                self.resetBody()
                self.placeApple()
                self._gameOver = False
