#Load driver for your hardware, visualizer just for example
# from bibliopixel.drivers.visualizer import DriverVisualizer
# driver = DriverVisualizer(num = 10)

from bibliopixel.drivers.serial_driver import *
driver = DriverSerial(LEDTYPE.APA102, 100, c_order=ChannelOrder.RGB, SPISpeed=16, deviceID=0)

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
	# while True:
	# 	led.fill(colors.Red, start=0, end=-1)
	# 	led.update()
	# 	time.sleep(1)
	# 	led.fill(colors.Green, start=0, end=-1)
	# 	led.update()
	# 	time.sleep(1)
	# 	led.fill(colors.Blue, start=0, end=-1)
	# 	led.update()
	# 	time.sleep(1)
	# 	led.fill(colors.White, start=0, end=-1)
	# 	led.update()
	# 	time.sleep(1)
	anim.run(fps = 5)
except KeyboardInterrupt:
	led.all_off()
	led.update()

