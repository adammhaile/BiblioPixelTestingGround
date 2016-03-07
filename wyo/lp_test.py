from bibliopixel.drivers.visualizer import DriverVisualizer
from bibliopixel.drivers.serial_driver import DriverSerial, LEDTYPE, ChannelOrder
from bibliopixel.animation import BaseStripAnim
from BiblioPixelAnimations.strip.LarsonScanners import LarsonScanner
from BiblioPixelAnimations.strip.Rainbows import RainbowCycle
from BiblioPixelAnimations.strip.ColorWipe import ColorWipe
from bibliopixel import LEDStrip
import bibliopixel.colors as colors
from system_eq import EQ
import bibliopixel.log as log
import time
log.setLogLevel(log.DEBUG)


class AudioTest(BaseStripAnim):

    def __init__(self, led, color_list, max_freq=4000, log_scale=True, auto_gain=False, gain=3):

        super(AudioTest, self).__init__(led)

        self.color_list = color_list
        bins = self._led.numLEDs
        self.source = EQ(bins=bins, max_freq=max_freq,
                         log_scale=log_scale, auto_gain=auto_gain, gain=gain)
        self.levels = [int((i * 255.0) / 1023.0) for i in range(1024)]

    def preRun(self, amt=1):
        self.source.start()

    def _exit(self, type, value, traceback):
        self.source.stop()

    def step(self, amt=1):
        self._led.all_off()
        data = self.source.get_audio_data()
        #base_c = colors.hue2rgb(self._step % 255)
        for i in range(len(data)):
            c = self.color_list[i % len(self.color_list)]
            #c = colors.color_scale(base_c, self.levels[data[i]])
            # c = colors.hue2rgb(self.levels[data[i]])
            c = colors.color_scale(c, self.levels[data[i]])

            self._led.set(i, c)
        self._step += 1

rainbow = [colors.Red, colors.Orange,
           colors.Yellow, colors.Green,
           colors.Blue, colors.Indigo,
           colors.Violet]

# driver = DriverVisualizer(num=33 * 7, pixelSize=30, stayTop=True)
driver = DriverSerial(LEDTYPE.WS2801, 1, dev="", c_order=ChannelOrder.RGB, SPISpeed=2, gamma=None, restart_timeout=3, deviceID=None, hardwareID="1D50:60AB")
led = LEDStrip(driver, threadedUpdate=False, masterBrightness=255, pixelWidth=1)

try:
    while True:
        led.fill(colors.Red)
        led.update()
        time.sleep(2)
        led.fill(colors.Green)
        led.update()
        time.sleep(2)
        led.fill(colors.Blue)
        led.update()
        time.sleep(2)
        led.fill(colors.White)
        led.update()
        time.sleep(2)
        led.fill(colors.Off)
        led.update()
        time.sleep(1)
        # anim = AudioTest(led, rainbow, max_freq=1200, log_scale=True, auto_gain=False, gain=25)
        # anim.run(fps=20)
        # anim = LarsonScanner(led, colors.Red, tail=2)
        # anim.run(fps=10, seconds=4)
        anim = RainbowCycle(led)
        anim.run(amt=6, fps=30, seconds=15)
        # anim = ColorWipe(led, colors.Red)
        # anim.run(fps=10, seconds=4)
        # led.all_off()
        # led.update()
        led.fill(colors.Off)
        led.update()
        time.sleep(1)
except:
    led.all_off()
    led.update()
