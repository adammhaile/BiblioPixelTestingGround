from bibliopixel import *
from bibliopixel.drivers.visualizer import DriverVisualizer
import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors

from noise import pnoise3, snoise3


class PerlinNoise(BaseMatrixAnim):

    def __init__(self, led, freq=16, octaves=1):
        super(PerlinNoise, self).__init__(led)
        self._step = 1
        self._freq = float(freq)
        self._octaves = octaves

    def step(self, amt):
        octaves = 1
        freq = 16.0
        data = []
        for y in range(self.height):
            for x in range(self.width):
                v = int(pnoise3(x / self._freq, y / self._freq, self._step / self._freq, octaves=self._octaves) * 127.0 + 128.0)
                c = colors.hue2rgb_rainbow(v)
                self._led.set(x,y, c)

        self._step += amt

driver = DriverVisualizer(width=25, height=50)
led = LEDMatrix(driver, serpentine=False, threadedUpdate=True, masterBrightness=255)

anim = PerlinNoise(led, freq=32)
anim.run(fps=20)
