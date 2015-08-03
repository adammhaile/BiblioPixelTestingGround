import bibliopixel.colors as colors
from bibliopixel.animation import BaseGameAnim
import math
from random import randint
import bibliopixel.util as util
import time

class Flappy(BaseGameAnim):
    def __init__(self, led, inputDev):
        super(Flappy, self).__init__(led, inputDev)

        self._speed = 5
        self._accel = 5

        self.setSpeed("add_pipe", 16)
        self.setSpeed("scroll", 5)

        self.addKeyFunc("FIRE", self.flap, speed=1, hold=False)
        self.addKeyFunc("X", self.togglePause, speed=1, hold=False)

        self.init_game()
        self.start_game()

    def init_game(self):
        self.setSpeed("scroll", 5)
        self.gameover = False
        self.levelUp = True
        self.doStart = False
        self.doStartTime = time.time()
        self.paused = True
        self.level = 1
        self.score = 0
        self._pipes = []
        self._pos = self.height/2
        self._x = self.width/2

    def start_game(self):
        self.doStart = False
        if self.gameover:
            self.init_game()
            self.gameover = False

    def clearLevelUp(self):
        self.doStart = False
        if self.levelUp:
            self.paused = False
            self.levelUp = False

    def nextLevel(self):
        self.level += 1
        self.levelUp = True
        self.paused = True
        s = self.getSpeed("scroll")
        s -= 1
        if s <= 0:
            self.win = True
        else:
            self.setSpeed("scroll", s)

    def togglePause(self):
        self.paused = not self.paused

    def flap(self):
        self._speed = self._accel*-1

    def moveBird(self):
        s = self._speed
        if s < 0:
            s += (self._accel+1)
        if self._checkSpeed(s):
            if self._speed > 0:
                self._pos += 1
                self._speed -= 1
            else:
                self._pos -= 1
                self._speed += 1
            if self._speed == 0: self._speed = 1

            if self._pos >= self.height or self._pos < 0:
                self.gameover = True
            else:
                for i in range(len(self._pipes)):
                    x,y = self._pipes[i]
                    if x == self._x:
                        if self._pos <= y or self._pos >= y+self.height/3:
                            self.gameover = True
                        else:
                            self.score += 5
                            if self.score % 200 == 0:
                                self.nextLevel()

    def addPipe(self):
        y = randint(self.height/2 - self.height/4, self.height/2)
        self._pipes.append((self.width, y))

    def scroll(self):
        for i in range(len(self._pipes)):
            x,y = self._pipes[i]
            x -= 1
            self._pipes[i] = (x,y)

        if len(self._pipes) > 0 and self._pipes[0][0] < 0:
            del self._pipes[0]

    def drawPipes(self):
        for p in self._pipes:
            self._led.drawLine(p[0], 0, p[0], p[1], colors.Green)
            self._led.drawLine(p[0], p[1]+self.height/3, p[0], self.height-1, colors.Green)

    def drawBird(self):
        self._led.set(self._x,self._pos,colors.Red)

    def drawScore(self):
        s = "{}".format(self.score)
        self._led.drawText(s, self.width/2-(len(s)*4)/2+1, 0, size=0, color=colors.Blue   )

    def step(self, amt=1):

        if (self.levelUp or self.gameover) and (self._lastKeys != self._keys) and any(v == True for v in self._keys.itervalues()) and (time.time() - self.doStartTime > 1):
            self.doStart = True
            self.doStartTime = time.time()
        if self.doStart:
            if not any(v == True for v in self._keys.itervalues()):
                if self.levelUp:
                    self.clearLevelUp()
                elif self.gameover:
                    self.start_game()
            else:
                return

        if not self.doStart:
            self.handleKeys()

        self._led.all_off()
        if self.gameover:
            self.drawBird()
            self.drawPipes()
            self._led.drawText("GAME", self.width/2-11, self.height/2-8, color=colors.Blue)
            self._led.drawText("OVER", self.width/2-11, self.height/2+1, color=colors.Blue)
            s = "{}".format(self.score)
            self._led.drawText(s, self.width/2-(len(s)*4)/2+1, self.height/2+9, size=0, color=colors.Blue )
        else:
            if self.paused:
                self._led.all_off()
                if self.levelUp:
                    self.drawPipes()
                    self._led.drawText("LVL", self.width/2-8, self.height/2-8, color=colors.Blue )
                    l = "{}".format(self.level)
                    self._led.drawText(l, self.width/2-(len(l)*6)/2+1, self.height/2+1, color=colors.Blue)
                else:
                    x = self.width/2-2
                    y = 1
                    self._led.drawText("P", x, y+0)
                    self._led.drawText("A", x, y+8)
                    self._led.drawText("U", x, y+16)
                    self._led.drawText("S", x, y+24)
                    self._led.drawText("E", x, y+32)
                    self._led.drawText("D", x, y+40)

            else:
                self.moveBird()
                self.drawBird()
                self.drawPipes()
                self.drawScore()

                if self.checkSpeed("add_pipe") and (randint(0,30)%5==0 or len(self._pipes) <= 1):
                    self.addPipe()

                if self.checkSpeed("scroll"):
                    self.scroll()
