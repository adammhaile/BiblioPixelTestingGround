from bibliopixel.led import *
import bibliopixel.image as img
from bibliopixel.drivers.serial_driver import *
import bibliopixel.gamma as gamma

#Takes a matrix and displays it as individual columns over time
class LEDPOV(LEDMatrix):

    def __init__(self, driver, povHeight, width, rotation = MatrixRotation.ROTATE_0, vert_flip = False):
        self.numLEDs = povHeight * width

        super(LEDPOV, self).__init__(driver, width, povHeight, None, rotation, vert_flip, False)
    
    #This is the magic. Overriding the normal update() method
    #It will automatically break up the frame into columns spread over frameTime (ms)    
    def update(self, frameTime = None):
        if frameTime:
            self._frameTotalTime = frameTime

        sleep = None
        if self._frameTotalTime:
            sleep = (self._frameTotalTime - self._frameGenTime) / self.width

        width = self.width
        for h in range(width):
            start = time.time() * 1000.0

            buf = [item for sublist in [self.buffer[(width*i*3)+(h*3):(width*i*3)+(h*3)+(3)] for i in range(self.height)] for item in sublist]
            self.driver.update(buf)
            sendTime = (time.time() * 1000.0) - start
            if sleep:
                time.sleep(max(0, (sleep - sendTime) / 1000.0))

#convert 6 character hex colors to RGB tuple
def hex2rgb(hex):
    """Helper for converting RGB and RGBA hex values to Color"""
    hex = hex.strip('#')
    if len(hex) == 6:
        split = (hex[0:2],hex[2:4],hex[4:6])
    else:
        raise ValueError('Must pass in either a 6 character hex value!')

    r, g, b = [int(x, 16) for x in split]

    return (r, g, b)

argv = sys.argv
argc = len(argv)

file = ""
bright = 255
col_time = 50
bgcolor = (0,0,0)

#load in command line args
if argc > 1:
    file = argv[1]
else:
    print "Must specifiy an input file!"
    sys.exit(2)

#get brightness value
if argc > 2:
    bright = int(x=argv[2])

#col_time is time to display each vertical line for, in ms
if argc > 3:
    col_time = int(argv[3])

#bgcolor is the color that will be used on transparent pixels
if argc > 4:
    bgcolor = hex2rgb(argv[4])

#open the file so it is not loaded each time through
i = img.Image.open(file)

img_width = i.size[0]
totalFrameTime = img_width * col_time

print "Image Display Time: {0:.1f}s".format(totalFrameTime/1000.0)

driver = DriverSerial(LEDTYPE.LPD8806, num = 96, c_order=ChannelOrder.BRG, SPISpeed=16, gamma=gamma.LPD8806)
led = LEDPOV(driver, povHeight = 96, width = img_width, rotation=MatrixRotation.ROTATE_0, vert_flip=True)
led.setMasterBrightness(bright)

img.showImage(led, imageObj = i, bgcolor=bgcolor)

try:
    while True:
        led.update(frameTime=totalFrameTime)
except KeyboardInterrupt:
    led.all_off()
    led.update()

