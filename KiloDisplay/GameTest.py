import bibliopixel.colors as colors
from bibliopixel.animation import BaseGameAnim
from GamePadEmu import GamePadEmu

class GameTest(BaseGameAnim):
    def __init__(self, led, inputDev, toroidal = True):
        super(GameTest, self).__init__(led, inputDev)
        self.toroidal = toroidal
        self._x = 0
        self._y = 5
        self._shipColor = colors.Red
        self._misColor = colors.Blue
        self.missiles = []

    def drawShip(self):
        x = self._x
        y = self._y
        c = self._shipColor
        self._led.set(x, y, c)
        for x in range(x-1, x+2):
            self._led.set(x, y+1, c)

    def drawMissiles(self):
        removals = []
        for i in range(len(self.missiles)):
            m = self.missiles[i]
            x, y = m
            self._led.set(x, y, self._misColor)
            y -= 1
            if y < 0:
                removals.append(m)
            else:
                self.missiles[i] = (x, y-1)

        for r in removals:
            self.missiles.remove(r)


    def step(self, amt=1):
        y = self._y
        x = self._x
        if self._keys.UP:
            y -= 1
        if self._keys.DOWN:
            y += 1
        if self._keys.RIGHT:
            x += 1
        if self._keys.LEFT:
            x -= 1

        if y >= self.height:
            y = 0 if self.toroidal else (self.height-1)
        elif y < 0:
            y = (self.height - 1) if self.toroidal else 0
        if x >= self.width:
            x = 0 if self.toroidal else (self.width-1)
        elif x < 0:
            x = (self.width - 1) if self.toroidal else 0

        self._x = x
        self._y = y

        if self._keys.RED:
            self.missiles.append((x,y-1))

        self._led.all_off()
        self.drawShip()
        self.drawMissiles()

if __name__ == "__main__":
    import time
    from bibliopixel import LEDMatrix
    from bibliopixel.drivers.visualizer import DriverVisualizer
    with GamePadEmu() as pad:
        driver = DriverVisualizer(num=0, width=32, height=32, pixelSize=15, port=1618, stayTop=True)
        led = LEDMatrix(driver, serpentine=True, threadedUpdate=True)
        anim = GameTest(led, pad, toroidal=False)
        try:
            anim.run(fps=20)
        except KeyboardInterrupt:
            led.all_off()
            led.update()
            time.sleep(1)
