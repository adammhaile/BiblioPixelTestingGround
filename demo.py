#!/usr/bin/python
import time
from bibliopixel.drivers.visualizer import *
from bibliopixel.drivers.serial_driver import *
from bibliopixel import *
from matrix_animations import *
from strip_animations import *
from GameOfLife import GameOfLife, GameOfLifeRGB
from TicTacToe import TicTacToe
from langton import LangtonsAnt
from bibliopixel.image import *
import bibliopixel.gamma as gamma

import bibliopixel.log as log
log.setLogLevel(log.logging.DEBUG)

#driver = DriverVisualizer(width = 32, height = 32, stayTop = True)
driver = DriverSerial(LEDTYPE.LPD8806, num = 32*32, dev="COM7")
led = LEDMatrix(driver, serpentine=False)
led.setMasterBrightness(128)

_cont = False

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
OFF = (0, 0, 0)

_rainbow = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Indigo, colors.Violet]

cx = float(led.width - 1) / 2
cy = float(led.height - 1) / 2

def golSingle():
    anim = GameOfLife(led)
    anim.run(max_steps = 0 if _cont else 100, fps=30)

def golRGB():
    anim = GameOfLifeRGB(led)
    anim.run(max_steps = 0 if _cont else 100, fps=30)

def langton():
    anim = LangtonsAnt(led)
    anim.run(max_steps = 0 if _cont else 400, fps=60)

def Matrix():
    anim = MatrixRain(led, growthRate = 4) 
    anim.run(fps = 15, max_steps=0 if _cont else 50)

def MatrixWater():
    anim = MatrixRain(led, colors = [(170, 192, 192)], growthRate = 4) 
    anim.run(fps = 10, max_steps=0 if _cont else 50)

def MatrixMultiColor():
    anim = MatrixRain(led, growthRate = 4, colors = _rainbow)
    anim.run(fps = 15, max_steps=0 if _cont else 50)

def MatrixRainbow():
    anim = MatrixRainBow(led)
    anim.run(fps = 15, max_steps=0 if _cont else 50)

def BloomOut():
    anim = Bloom(led, dir = False)
    anim.run(amt = 4, max_steps = 0 if _cont else 192, fps=60)

def BloomIn():
    anim = Bloom(led, dir = True)
    anim.run(amt = 8, max_steps = 0 if _cont else 192, fps=60)

def TriangleSpin():
    anim = SpiningTriangle(led, cx, cy, 15)
    anim.run(amt = 6, max_steps = 0 if _cont else 180, fps = 30)


def ttt():
    anim = TicTacToe(led)
    anim.run(fps = 2, untilComplete = not _cont)

#GIF Animations 
def adaLogo():
    showImage(led, imageObj = adaLogo.img)
    led.update()
    time.sleep(3)
adaLogo.img = Image.open("./anims/ada_logo.png")

# def MLLogo():
#     MLLogo.anim.run(untilComplete = not _cont)
# MLLogo.anim = ImageAnim(led, "./anims/ML_GIF.gif")


# def pacman():
#     pacman.anim.run(untilComplete = not _cont, max_cycles = 10)
# pacman.anim = ImageAnim(led, "./anims/pacman.gif")

# def Metroid():
#     Metroid.anim.run(untilComplete = not _cont, max_cycles = 8)
# Metroid.anim = ImageAnim(led, "./anims/Metroid.gif")

# def mario_run():
#    mario_run.anim.run(untilComplete = not _cont, max_cycles = 10, fps = 10)
# mario_run.anim = ImageAnim(led, "./anims/mario_run.gif")

# def ParaGoomba():
#     ParaGoomba.anim.run(untilComplete = not _cont, max_cycles = 10)
# ParaGoomba.anim = ImageAnim(led, "./anims/ParaGoomba.gif", bgcolor = colors.color_scale((135, 206, 235), 50))

def yoshi():
   yoshi.anim.run(untilComplete = not _cont, max_cycles = 2)#, fps = 10)
yoshi.anim = ImageAnim(led, "./anims/YoshiRotating.gif")

def bowser():
   bowser.anim.run(untilComplete = not _cont, max_cycles = 2)#, fps = 10)
bowser.anim = ImageAnim(led, "./anims/BowserRotating.gif")

def luigi():
   luigi.anim.run(untilComplete = not _cont, max_cycles = 2)#, fps = 10)
luigi.anim = ImageAnim(led, "./anims/LuigiRotating.gif")

def mario():
   mario.anim.run(untilComplete = not _cont, max_cycles = 2)#, fps = 10)
mario.anim = ImageAnim(led, "./anims/MarioRotating.gif")

def plant():
   plant.anim.run(untilComplete = not _cont, max_cycles = 6)#, fps = 10)
plant.anim = ImageAnim(led, "./anims/PiranhaPlantU.gif")

#End GIF Animations

_anims = [
    # ("Adafruit", adaLogo),
    ("Matrix", Matrix),
    # ("Matrix Water", MatrixWater),
    # ("Matrix Multi Color", MatrixMultiColor),
    ("Matrix Rainbow", MatrixRainbow),
    ("Bloom In", BloomIn),
    ("Bloom Out", BloomOut),
    ("Triangle Spin", TriangleSpin),
    # ("Triangle Blend", TriangleBlend),
    # ("Triangle Dual", TriangleDual),
    ("Game of Life Single", golSingle),
    ("Game of Life RGB", golRGB),
    ("Langton's Ant", langton),
    ("Yoshi", yoshi),
    ("Luigi", luigi),
    ("Bowser", bowser),
    ("Mario", mario),
    ("Plant", plant),
    # ("Metroid", Metroid),
    # ("PacMan", pacman),
    # ("Mario Run", mario_run),
    # ("ParaGoomba", ParaGoomba)
]

def doDemo():
    global _cont
    _cont = False
    try:
        while True:
            for a in _anims:
                led.all_off()
                a[1]()
    except KeyboardInterrupt:
        pass

    led.all_off()
    led.update()

def printMenu():
    print ""
    print "0 - Demo Mode"
    for i in range(0, len(_anims)):
        print str(i+1) + " - " + _anims[i][0]

def doAnim(index):
    global _cont
    _cont = True
    try:
        led.all_off()
        _anims[index][1]()
    except KeyboardInterrupt:
        pass

    led.all_off()
    led.update()

def handleMenu(choice):
    try:
        i = int(choice)
        if i <= len(_anims):
            if i == 0:
                doDemo()
            else:
                doAnim(i-1)
        else:
            raise ValueError()
    except ValueError:
        print "Invalid Option!"

try:
    while True:
        printMenu()
        i = raw_input("Choice: ")
        handleMenu(i)

except KeyboardInterrupt:
    pass

print "\nDone!\n"
led.all_off()
led.update()