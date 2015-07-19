import time
from bibliopixel.drivers.serial_driver import *
drivers = []

drivers.append(DriverSerial(LEDTYPE.NEOPIXEL, 25*25, c_order=ChannelOrder.RGB, deviceID=0))
drivers.append(DriverSerial(LEDTYPE.NEOPIXEL, 25*25, c_order=ChannelOrder.RGB, deviceID=1))

import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

from bibliopixel.led import *
import bibliopixel.colors as colors

gen = MultiMapBuilder()
gen.addRow(mapGen(25, 25, rotation = MatrixRotation.ROTATE_90, vert_flip = True))
gen.addRow(mapGen(25, 25, rotation = MatrixRotation.ROTATE_90, vert_flip = False))

#load the LEDStrip class
from bibliopixel.led import *
led = LEDMatrix(drivers, width=25, height=25*len(drivers), coordMap = gen.map, threadedUpdate=True)
led.setMasterBrightness(128)

from matrix_animations import *
anim = Bloom(led)

from GameOfLife import *
anim = GameOfLifeRGB(led)

from BiblioPixelAnimations.matrix import opencv_video

from bibliopixel.animation import MatrixCalibrationTest

# from strip_animations import *
# anim = RainbowCycle(led, start=0, end=-1)

try:
	#anim = opencv_video.OpenCVVideo(led, videoSource = "getlucky.avi", mirror = False, offset = 0.0, crop=True, useVidFPS=True)
	#anim = MatrixCalibrationTest(led)
	anim.run(amt=6, fps=10)
except KeyboardInterrupt:
	led.all_off()
	led.update()
	time.sleep(0.5)
	led.all_off()
	led.update()
	time.sleep(0.5)
