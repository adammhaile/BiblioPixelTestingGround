from bibliopixel import *
from bibliopixel.drivers.serial_driver import *
from bibliopixel.animation import *

class ChipsetTest(BaseStripAnim):
    def __init__(self, led):
        super(ChipsetTest, self).__init__(led)
        self._internalDelay = 250
        self.colors =  [colors.Red, colors.Green, colors.Blue]
  
    def step(self, amt = 1):
        
        if self._step % 4 != 0:
            for i in range(self._led.numLEDs):
                self._led.set(i, self.colors[i%3])
        else:
            led.all_off()

        self._step += 1

cs = [
	# [LEDTYPE.TM1809, ChannelOrder.RGB, "TM1809"],
	# [LEDTYPE.UCS1903, ChannelOrder.RGB, "UCS1903"],
	# [LEDTYPE.SM16716, ChannelOrder.RGB, "SM16716"],
	# [LEDTYPE.APA102, ChannelOrder.BGR, "APA102"],
	# [LEDTYPE.WS2801, ChannelOrder.RGB, "WS2801"],
 #    [LEDTYPE.LPD8806, ChannelOrder.BRG, "LPD8806"],
    [LEDTYPE.WS2812, ChannelOrder.GRB, "WS2812"],
    [LEDTYPE.LPD1886, ChannelOrder.RGB, "LPD1886"],
]

for c in cs:
	print "\nTesting: {}".format(c[2])
	raw_input("Disconnect from strip...")
	driver = DriverSerial(c[0], 10, c_order=c[1], SPISpeed=2)
	raw_input("Connect to strip...")
	led = LEDStrip(driver)
	led.setMasterBrightness(128)

	anim = ChipsetTest(led)

	try:
	    anim.run(max_steps=16)
	    led.all_off()
	    led.update()
	except KeyboardInterrupt:
	    led.all_off()
	    led.update()

	driver._com.close()
