import sys

ID = 0
num = 100

if len(sys.argv) > 1:
	ID = int(sys.argv[1])
if len(sys.argv) > 2:
	num = int(sys.argv[2])

from bibliopixel.drivers.serial_driver import *
driver = DriverSerial(LEDTYPE.APA102, num, c_order=ChannelOrder.RGB, SPISpeed=16, deviceID=ID)

import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

import bibliopixel.colors as colors

#load the LEDStrip class
from bibliopixel.led import *
led = LEDStrip(driver)

#load channel test animation
# from bibliopixel.animation import StripChannelTest
# anim = StripChannelTest(led)

from strip_animations import *
anim = RainbowCycle(led, start=0, end=-1)

try:
	anim.run(fps = 5)
except KeyboardInterrupt:
	led.all_off()
	led.update()

