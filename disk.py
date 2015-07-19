from bibliopixel import *
from bibliopixel.animation import BaseStripAnim, StripChannelTest

import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

class DiskBloom(BaseStripAnim):

    def __init__(self, led, dir = True):
        super(DiskBloom, self).__init__(led)
        self._dir = dir
        self.rings = [
            [0,47],     #48
            [48,91],    #44
            [92,131],    #40
            [132,163],    #32
            [164,191],    #28
            [192,215],    #24
            [216,235],    #20
            [236,247],    #12
            [248,253],    #6
            [254,254],    #1
        ]
        self.ringCount = len(self.rings) 

    def step(self, amt = 8):
        if self._dir:
            s = 255 - self._step
        else:
            s = self._step

        for i in range(self.ringCount):
            c = colors.hue_helper(i, self.ringCount, s)
            self._led.fill(c, self.rings[i][0], self.rings[i][1])

        self._step += amt
        if(self._step >= 255):
            self._step = 0


import bibliopixel.gamma as gamma
from bibliopixel.drivers.serial_driver import *

driver = DriverSerial(LEDTYPE.APA102, 255, c_order=ChannelOrder.BGR, SPISpeed=2)
led = LEDStrip(driver, threadedUpdate=True)
led.setMasterBrightness(32)

try:
    anim = DiskBloom(led, dir=False)
    anim = StripChannelTest(led)
    anim.run()#amt=6, fps=60)
except KeyboardInterrupt:
    led.all_off()
    led.update()
    time.sleep(0.5)

