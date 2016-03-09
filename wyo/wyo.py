if __name__ == "__main__":
    import wyo_controller
    from bibliopixel import LEDMatrix
    from bibliopixel.drivers.serial_driver import DriverSerial, LEDTYPE, ChannelOrder
    import bibliopixel.colors as colors
    import bibliopixel.log as log
    import time
    import os

    log.setLogLevel(log.DEBUG)

    w = NUM_LEDS_PER_STRIP = wyo_controller.width
    h = NUM_STRIPS = wyo_controller.height
    hw_id = "16C0:0483"

    try:
        drivers = [
            DriverSerial(LEDTYPE.GENERIC, w * h, deviceID=0, hardwareID=hw_id),
            DriverSerial(LEDTYPE.GENERIC, w * h, deviceID=1, hardwareID=hw_id),
            DriverSerial(LEDTYPE.GENERIC, w * h, deviceID=2, hardwareID=hw_id),
        ]
        params = wyo_controller.genDisplayParams()
    except:
        raise
        from bibliopixel.drivers.visualizer import DriverVisualizer
        os.system("start Vis.exe 64 48")
        drivers = [DriverVisualizer(width=w, height=h * 3)]
        params = {
            "width": w,
            "height": h * 3,
            "serpentine": False
        }

    led = LEDMatrix(drivers, threadedUpdate=True, masterBrightness=32, **params)

    from BiblioPixelAnimations.matrix.bloom import Bloom
    from BiblioPixelAnimations.matrix.GameOfLife import GameOfLifeRGB
    from BiblioPixelAnimations.matrix.MatrixRain import MatrixRainBow
    from BiblioPixelAnimations.matrix.Text import ScrollText
    from BiblioPixelAnimations.matrix.Mainframe import Mainframe
    from BiblioPixelAnimations.matrix.perlin_simplex import PerlinSimplex
    from BiblioPixelAnimations.matrix.circlepop import CirclePop
    from BiblioPixelAnimations.matrix.LangtonsAnt import LangtonsAnt
    from BiblioPixelAnimations.matrix.ImageAnim import ImageAnim, ImageAnimFolder
    from system_eq import EQ
    from ScreenGrab import ScreenGrab
    testcolors = [colors.Red, colors.Green,
                  colors.Blue, colors.White, colors.Off]

    from msgeq7 import MSGEQ7, DummyData
    from spectrum import Spectrum, Spread, BasicLineGraph, PeakLineGraph
    rainbow = [colors.Red, colors.Orange,
               colors.Yellow, colors.Green,
               colors.Blue, colors.Indigo,
               colors.Violet]

    anim = None
    try:

        # anim = EQ(led)
        # anim.run(fps=30)

        #eq = MSGEQ7(lower_threshold = 70)
        anim = Spectrum(led, steps_per_vis=50, bins=64, max_freq=2000, gain=3)
        anim.run(fps=15)
        #
        # anim = ScreenGrab(led, bbox =(1920,0,1920+1024,768), mirror = False, offset = 0.0, crop = True)
        # anim.run(fps=12)
        # anim = ScrollText(led, "WyoManiacal", xPos=NUM_LEDS_PER_STRIP/2, yPos=0, color=colors.White)
        while True:
            # anim = ImageAnimFolder(led, "./anims", cycles=3)
            # anim.run()
            #anim = ImageAnim(led, imagePath="./anims/zelda.gif")
            #anim.run()#untilComplete=True, max_cycles=20)
            # anim = LangtonsAnt(led, antColor=colors.Green, pathColor=colors.Red)
            # anim.run(fps=30, seconds=5.4)#, max_steps=75)
            anim = CirclePop(led)
            anim.run(fps=30, seconds=5)
            anim = Mainframe(led, scroll = False)
            anim.run(fps=5, max_steps=40)
            anim = PerlinSimplex(led, freq=32, octaves=1, type=True)
            anim.run(fps=30, seconds=5)
            anim = Bloom(led, dir=True)
            anim.run(fps=30, amt=6, seconds=5)
            anim = GameOfLifeRGB(led, toroidal=True)
            anim.run(amt=1, fps=15, seconds=5)
            anim = MatrixRainBow(led, tail=4, growthRate=7)
            anim.run(amt=1, fps=20, seconds=5)
            print "done"
    except KeyboardInterrupt, e:
        print e
        print "exce"
        anim.cleanup()
        led.all_off()
        led.update()
        time.sleep(1)

    print "all off"
    led.all_off()
    led.update()
    time.sleep(1)
