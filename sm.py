from bibliopixel import LEDMatrix
from bibliopixel.drivers.serial_driver import DriverSerial, ChannelOrder, LEDTYPE
import bibliopixel.colors as colors
import time

driver = DriverSerial(LEDTYPE.GENERIC, 32*32, hardwareID="16C0:0483")
led = LEDMatrix(driver, width=32, height=32, serpentine=False)

print "Red"
led.fill(colors.Red)
led.update()
time.sleep(1)

print "Green"
led.fill(colors.Green)
led.update()
time.sleep(1)

print "Blue"
led.fill(colors.Blue)
led.update()
time.sleep(1)

print "Off"
led.fill(colors.Off)
led.update()
time.sleep(1)
