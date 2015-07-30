import bibliopixel.colors as colors
from bibliopixel.animation import BaseGameAnim
import math
from random import randint
import bibliopixel.util as util

class Snake(BaseGameAnim):
    def __init__(self, led, inputDev):
        super(Snake, self).__init__(led, inputDev)
        self._growLen = 3
        self._speed = 0.4
        self._speedGrow = 0.1
        self._lives = 4
        self._level = 1
        self._apCount = 0
        self._apGoal = 6
        self._lastKeys = None
        self._apple = (-1, -1)
        self._gameOver = False
        self._gameOverCount = 0
        self._levelUp = True
        self._growCount = 0
        self._directions = [(0,-1), (0,1), (1,0), (-1,0)]

        self.setSpeed("move", 4)

        self.resetBody()
        self.placeApple()

    def drawBody(self):
        l = len(self._body)
        i = 0
        for b in self._body:
            c = colors.hue_helper(i, l, 1)
            x,y = b
            self._led.set(x, y, c)
            i += 1

    def drawLives(self):
        for i in range(self._lives):
            self._led.set(self.width-1-i*2, 0, colors.Red)

    def drawApplesLeft(self):
        for i in range(self._apGoal - self._apCount):
            self._led.set(i*2, 0, colors.Green)

    def drawApple(self):
        x,y = self._apple
        self._led.set(x, y, colors.Green)

    def resetBody(self):
        dx, dy = self._dir = self._directions[0]#randint(0,3)]
        dx, dy = dx*-1, dy*-1
        x, y = self._pos = (self._led.width/2,self._led.height/2)
        self._body = []
        for i in range(self._growLen):
            self._body.append(((x+(i*dx)),(y+(i*dy))))
        self._newDir = None

    def gameOver(self):
        self._gameOver = True
        self._gameOverCount = 0
        self._levelUp = True
        self._level = 1
        self._speed = 0.3
        self._lives = 4


    def dead(self):
        self._apCount = 0
        self._lives -= 1
        self._levelUp = True
        if self._lives <= 0:
            self.gameOver()


    def nextLevel(self):
        self._apCount = 0
        self._levelUp = True
        self._level += 1
        s =  self.getSpeed("move") - 1
        if s<1: s=1
        self.setSpeed("move", s)
        # self._speed += self._speedGrow
        self.resetBody()

    def move(self):
        if self.checkSpeed("move"):
            x, y = self._pos = util.tuple_add(self._dir, self._pos)
            self._body.insert(0, (x,y))
            if (x,y) == self._apple:
                self._growCount = self._growLen
                self._apCount += 1
                self.placeApple()

            if self._growCount == 0:
                del self._body[-1]
            else:
                self._growCount -= 1

            if self._newDir:
                self._dir = self._newDir
                self._newDir = None

            if(x < 0 or x >= self.width or y < 1 or y >= self.height) or (x,y) in self._body[1:]:
                self.dead()
            else:
                if self._apCount >= self._apGoal:
                    self.nextLevel()

    def placeApple(self):
        while True:
            x = randint(1, self.width-2)
            y = randint(1, self.height-2)
            if (x,y) not in self._body:
                break
        self._apple = (x, y)

    def step(self, amt=1):
        if self._gameOver:
            self._led.all_off()
            self._led.drawText("GAME", self.width/2-11, self.height/2-8)
            self._led.drawText("OVER", self.width/2-11, self.height/2+1)
            self._gameOverCount += 1
            if self._gameOverCount > 45:
                self.resetBody()
                self.placeApple()
                self._gameOver = False
        elif self._levelUp:
            self._led.all_off()
            self._led.drawText("LVL", self.width/2-8, self.height/2-8)
            lvl = "{}".format(self._level)
            w = len(lvl)*6
            self._led.drawText(lvl, self.width/2-(w/2), self.height/2+1)
            if self._keys.FIRE:#any(v > 0 for v in self._keys.itervalues()):
                self._levelUp = False
                self.resetBody()
                self.placeApple()
                self._lastKeys = None
        else:
            if self._keys != self._lastKeys:
                self._pos = self._body[0]
                if self._keys.UP and self._dir[1] == 0:
                    self._newDir = self._directions[0]
                if self._keys.DOWN and self._dir[1] == 0:
                    self._newDir = self._directions[1]
                if self._keys.RIGHT and self._dir[0] == 0:
                    self._newDir = self._directions[2]
                if self._keys.LEFT and self._dir[0] == 0:
                    self._newDir = self._directions[3]

                self._lastKeys = self._keys

            self.move()
            self._led.all_off()
            self.drawBody()
            self.drawApple()
            self.drawApplesLeft()
            self.drawLives()
