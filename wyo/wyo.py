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
        from bibliopixel.drivers.visualizer import DriverVisualizer
        os.system("start Vis.exe 64 48")
        drivers = [DriverVisualizer(width=w, height=h * 3)]
        params = {
            "width": w,
            "height": h * 3,
            "serpentine": False
        }

    led = LEDMatrix(drivers, threadedUpdate=True,
                    masterBrightness=32, **params)

    from BiblioPixelAnimations.matrix.bloom import Bloom
    from BiblioPixelAnimations.matrix.GameOfLife import GameOfLifeRGB
    from BiblioPixelAnimations.matrix.MatrixRain import MatrixRainBow
    from BiblioPixelAnimations.matrix.Text import ScrollText
    from BiblioPixelAnimations.matrix.Mainframe import Mainframe
    from BiblioPixelAnimations.matrix.perlin_simplex import PerlinSimplex
    from BiblioPixelAnimations.matrix.circlepop import CirclePop
    from ScreenGrab import ScreenGrab
    testcolors = [colors.Red, colors.Green,
                  colors.Blue, colors.White, colors.Off]

    from msgeq7 import MSGEQ7
    from spectrum import Spectrum, BasicSpectrumGraph
    rainbow = [colors.Red, colors.Orange,
               colors.Yellow, colors.Green,
               colors.Blue, colors.Indigo,
               colors.Violet]
    try:
        # eq = MSGEQ7()
        # anim = Spectrum(led, audio_source=eq)
        # anim.set_draw_obj(BasicSpectrumGraph(anim, fill=True, colors=rainbow))
        # anim.run(fps=30)
        #
        # anim = ScreenGrab(led, bbox =(1920,0,1920+1024,768), mirror = False, offset = 0.0, crop = True)
        # anim.run(fps=15)
        # anim = ScrollText(led, "WyoManiacal", xPos=NUM_LEDS_PER_STRIP/2, yPos=0, color=colors.White)
        while True:
            anim = CirclePop(led)
            anim.run(fps=20)
            anim = Mainframe(led, scroll = False)
            anim.run(fps=5, max_steps=40)
            anim = PerlinSimplex(led, freq=32, octaves=1, type=True)
            anim.run(amt=1, fps=30, sleep=None, max_steps=100, untilComplete=False,
                     max_cycles=0, threaded=False, joinThread=False, callback=None)
            anim = Bloom(led, dir=True)
            anim.run(fps=30, amt=6, max_steps=100)
            anim = GameOfLifeRGB(led, toroidal=True)
            anim.run(amt=1, fps=15, sleep=None, max_steps=75, untilComplete=False,
                     max_cycles=0, threaded=False, joinThread=False, callback=None)
            anim = MatrixRainBow(led, tail=4, growthRate=7)
            anim.run(amt=1, fps=20, sleep=None, max_steps=150, untilComplete=False,
                     max_cycles=0, threaded=False, joinThread=False, callback=None)
            print "done"
    except KeyboardInterrupt, e:
        print e
        print "exce"
        led.all_off()
        led.update()
        time.sleep(1)

    print "all off"
    led.all_off()
    led.update()
    time.sleep(1)
