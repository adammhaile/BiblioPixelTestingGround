from bibliopixel import LEDStrip, colors
from bibliopixel.drivers.serial_driver import DriverSerial, LEDTYPE, ChannelOrder
import time
from bibliopixel import log
log.setLogLevel(log.DEBUG)

driver = DriverSerial(LEDTYPE.NEOPIXEL, 350, c_order=ChannelOrder.RGB)
led = LEDStrip(driver, threadedUpdate=False)
led.setMasterBrightness(192)

try:
    while True:
        led.fill(colors.Red)
        led.update()
        time.sleep(0.5)
        led.fill(colors.Green)
        led.update()
        time.sleep(0.5)
        led.fill(colors.Blue)
        led.update()
        time.sleep(0.5)
        led.fill(colors.White)
        led.update()
        time.sleep(0.5)
except KeyboardInterrupt:
    led.all_off()
    led.update()

#testing emoji
