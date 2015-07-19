import bibliopixel.colors as colors
from bibliopixel.animation import BaseGameAnim

class Snake(BaseGameAnim):
    def __init__(self, led, inputDev):
        super(Snake, self).__init__(led, inputDev)

        self.pos = (self._led.width/2,self._led.height/2)
        self._body = [self.pos, (self.pos[0], self.pos[1]+1)]

    def drawBody(self):
        for b in self._body:
            x,y = b
            self._led.set(x,y, colors.Red)

    def step(self, amt=1):
        # y = self._y
        # x = self._x
        # if self._keys.UP:
        #     y -= 1
        # if self._keys.DOWN:
        #     y += 1
        # if self._keys.RIGHT:
        #     x += 1
        # if self._keys.LEFT:
        #     x -= 1

        # if y >= self.height:
        #     y = 0 if self.toroidal else (self.height-1)
        # elif y < 0:
        #     y = (self.height - 1) if self.toroidal else 0
        # if x >= self.width:
        #     x = 0 if self.toroidal else (self.width-1)
        # elif x < 0:
        #     x = (self.width - 1) if self.toroidal else 0

        # self._led.all_off()
        self.drawBody()
