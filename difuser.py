from bibliopixel import *
import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

from strip_animations import *

from bibliopixel.drivers.serial_driver import *
driver = DriverSerial(LEDTYPE.NEOPIXEL, 1, c_order=ChannelOrder.RGB)

led = LEDStrip(driver, threadedUpdate=False)

try:
	anim = RainbowCycle(led, start=0, end=-1)
	anim.run(amt=1, fps=30)

except KeyboardInterrupt:
	led.all_off()
	led.update()