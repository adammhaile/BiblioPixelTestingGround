from bibliopixel import *
from bibliopixel.led import *
from bibliopixel.animation import BaseCircleAnim

class DiskBloom(BaseCircleAnim):

    def __init__(self, led, spread = 1):
        super(DiskBloom, self).__init__(led)
        self._dir = dir
        self.spread = spread

    def step(self, amt = 8):
        for i in range(self.ringCount):
            c = colors.hue_helper(i, int(self.ringCount * self.spread), self._step)
            self._led.fillRing(i, c)

        self._step += amt
        if(self._step >= 255):
            self._step = 0

class ArcRotate(BaseCircleAnim):

    def __init__(self, led, colors, arc = 180, outterRing = -1):
        super(ArcRotate, self).__init__(led)
        if outterRing < 0 or outterRing > self._led.lastRing:
            outterRing = self._led.lastRing
        self.outterRing = outterRing
        self.colors = colors
        self.arcCount = len(self.colors)
        self.arc = arc/2

    def step(self, amt = 1):
        led.all_off()
        ci = 0
        for r in range(self.outterRing, self.outterRing - self.arcCount, -1):
            c = self.colors[ci]
            ci += 1
            self._led.fillRing(r, c, startAngle=self._step-self.arc, endAngle=self._step+self.arc)
        self._step += amt
        self._step %= 360

class PacMan(BaseCircleAnim):

    def __init__(self, led, color, maxOpen = 90, outterRing = -1):
        super(PacMan, self).__init__(led)
        if outterRing < 0 or outterRing > self._led.lastRing:
            outterRing = self._led.lastRing
        self.outterRing = outterRing
        self.color = color
        self.eyeColor = (0,0,0)
        self.eyePoint = int((self.outterRing+1)/2)
        self.maxOpen = maxOpen/2
        self._dir = 1

    def step(self, amt = 8):
        led.all_off()
        for r in range(self.outterRing + 1):
            self._led.fillRing(r, self.color, startAngle=90+self._step+self._led.ringSteps[self.outterRing], endAngle=90-self._step)

        self._led.drawRadius(self._led.ringSteps[self.outterRing]*3, self.eyeColor, self.eyePoint, self.eyePoint)

        if self._step >= self.maxOpen or (self._dir < 1 and self._step < 5):
            self._dir = self._dir * -1
        self._step += (amt * self._dir)


import time
class ArcClock(BaseCircleAnim):

    def __init__(self, led, secRing = -1, minRing = -1, hourRing = -1):
        super(ArcClock, self).__init__(led)
        self._internalDelay = 250 #only run 4 times per second
        self.hourRing = hourRing
        self.secRing = secRing
        if self.secRing < 0:
            self.secRing = self.lastRing
        self.minRing = minRing
        if self.minRing < 0:
            self.minRing = self.lastRing - 1
        if self.hourRing < 0:
            self.hourRing = self.lastRing - 2


    def step(self, amt = 1):
        led.all_off()
        t = time.localtime()
        h = t.tm_hour
        m = t.tm_min
        s = t.tm_sec

        self._led.fillRing(self.hourRing, colors.Red, startAngle=0, endAngle=(h%12)*(360/12))
        self._led.fillRing(self.minRing, colors.Green, startAngle=0, endAngle=m*(360/60))
        self._led.fillRing(self.secRing, colors.Blue, startAngle=0, endAngle=s*(360/60))

class RadiusClock(BaseCircleAnim):

    def __init__(self, led, secRing = -1, minRing = -1, hourRing = -1):
        super(RadiusClock, self).__init__(led)
        self._internalDelay = 250 #only run 4 times per second
        self.hourRing = hourRing
        self.secRing = secRing
        if self.secRing < 0:
            self.secRing = self.lastRing
        self.minRing = minRing
        if self.minRing < 0:
            self.minRing = self.lastRing - 1
        if self.hourRing < 0:
            self.hourRing = self.lastRing - 2


    def step(self, amt = 1):
        led.all_off()
        t = time.localtime()
        h = t.tm_hour
        m = t.tm_min
        s = t.tm_sec

        self._led.drawRadius(angle=(h%12)*(360/12), color = colors.Red, endRing = self.hourRing)
        self._led.drawRadius(angle=m*(360/60), color = colors.Green, endRing = self.minRing)
        self._led.drawRadius(angle=s*(360/60), color = colors.Blue, endRing = self.secRing)

class PinWheel(BaseCircleAnim):

    def __init__(self, led, colors, blades = 3, startRing=0, endRing = -1):
        super(PinWheel, self).__init__(led)
        self.colors = colors
        self.blades = blades
        self.sepDegrees = 360.0 / self.blades
        self.startRing = startRing
        self.endRing = endRing

    def step(self, amt = 1):
        led.all_off()
        for i in range(self.blades):
            self._led.drawRadius(angle=self._step + (i * self.sepDegrees), color = self.colors[i%len(self.colors)], startRing = self.startRing, endRing = self.endRing)

        self._step += amt
        self._step %= 360

rings = [
    [254,254],  #0 - Center Point
    [248,253],  #1
    [236,247],  #2
    [216,235],  #3
    [192,215],  #4
    [164,191],  #5
    [132,163],  #6
    [92,131],   #7
    [48,91],    #8
    [0,47],     #9 - Outer Ring
]

full_rings = []
for r in rings:
    full_rings.append(range(r[0], r[1]+1, 1))

def frange(start, end, step):
    while start < end:
        yield start
        start += step

if __name__ == '__main__':
    import bibliopixel.log as log
    log.setLogLevel(log.DEBUG)

    from bibliopixel.drivers.serial_driver import *
    import bibliopixel.gamma as gamma
    driver = DriverSerial(LEDTYPE.APA102, 255, c_order=ChannelOrder.BGR, gamma=gamma.APA102, SPISpeed=12)

    led = LEDCircle(driver, full_rings, threadedUpdate=False, rotation=0, maxAngleDiff = 0)
    led.setMasterBrightness(64)

    rainbow = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Purple]
    try:

        while True:
            anim = PinWheel(led, colors = rainbow, blades = 6, startRing=2)
            anim.run(amt = 7.5, fps = 45, max_steps=48*6)
            anim = PacMan(led, colors.Yellow, maxOpen=90, outterRing=-1)
            anim.run(amt=4, fps=45, max_steps=160)
            anim = DiskBloom(led, spread = 1)
            anim.run(amt=-6, fps=45, max_steps=160)
            anim = ArcRotate(led, colors = rainbow, arc=120, outterRing=-1)
            anim.run(amt=15, fps=30, max_steps=180)
            anim = ArcClock(led, secRing=-1, minRing=-1, hourRing=-1)
            anim.run(max_steps=50)
            # anim = RadiusClock(led, secRing=-1, minRing=-1, hourRing=-1)
            # anim.run(max_steps=50)

    except KeyboardInterrupt:
        led.all_off()
        led.update()
        time.sleep(0.5)
