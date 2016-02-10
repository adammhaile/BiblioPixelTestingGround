from bibliopixel import LEDMatrix, MultiMapBuilder, mapGen
from bibliopixel.drivers.serial_driver import DriverSerial, LEDTYPE, ChannelOrder
from BiblioPixelAnimations.matrix.bloom import Bloom
from BiblioPixelAnimations.matrix.GameOfLife import GameOfLifeRGB
from BiblioPixelAnimations.matrix.MatrixRain import MatrixRainBow
from BiblioPixelAnimations.matrix.Text import ScrollText
from ScreenGrab import ScreenGrab

import bibliopixel.colors as colors
import bibliopixel.log as log
import time

log.setLogLevel(log.DEBUG)

w = NUM_LEDS_PER_STRIP = 64
h = NUM_STRIPS = 16
hw_id = "16C0:0483"

gen = MultiMapBuilder()

drivers = [
    DriverSerial(LEDTYPE.GENERIC, w * h, deviceID=0, hardwareID=hw_id),
    DriverSerial(LEDTYPE.GENERIC, w * h, deviceID=1, hardwareID=hw_id),
    DriverSerial(LEDTYPE.GENERIC, w * h, deviceID=2, hardwareID=hw_id),
]

gen.addRow(mapGen(w, h, serpentine=False))
gen.addRow(mapGen(w, h, serpentine=False))
gen.addRow(mapGen(w, h, serpentine=False))

led = LEDMatrix(drivers, width=w, height=h * len(drivers),
                threadedUpdate=True, masterBrightness=32, coordMap=gen.map)
led.setMasterBrightness(16)
testcolors = [colors.Red, colors.Green, colors.Blue, colors.White, colors.Off]
try:
    anim = ScreenGrab(led, bbox =(1920,0,2720,600), mirror = False, offset = 0.0, crop = True)
    anim.run(fps=15)
    # anim = ScrollText(led, "WyoManiacal", xPos=NUM_LEDS_PER_STRIP/2, yPos=0, color=colors.White)
    while True:
        anim = Bloom(led, dir=True)
        anim.run(fps=30, amt=6, max_steps=100)
        anim = GameOfLifeRGB(led, toroidal = True)
        anim.run(amt = 1, fps=15, sleep=None, max_steps =75, untilComplete = False, max_cycles = 0, threaded = False, joinThread = False, callback=None)
        anim = MatrixRainBow(led, tail=4, growthRate=7)
        anim.run(amt = 1, fps=20, sleep=None, max_steps =150, untilComplete = False, max_cycles = 0, threaded = False, joinThread = False, callback=None)
    # print "done"
except KeyboardInterrupt, e:
    print e
    print "exce"
    led.all_off()
    led.update()
    time.sleep(1)

print "all off"
led.all_off()
led.update()
time.sleep(1)
