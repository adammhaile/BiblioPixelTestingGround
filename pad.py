from bibliopixel.drivers.visualizer import DriverVisualizer
from bibliopixel import *
import bibliopixel.log as log
# log.setLogLevel(log.DEBUG)

from bibliopixel.serial_gamepad import SerialGamePad
from bibliopixel.win_gamepad_emu import WinGamePadEmu
import time

driver = DriverVisualizer(width=25, height=50)
led = LEDMatrix(driver, serpentine=False, threadedUpdate=True)

from BiblioPixelAnimations.game.Tetris import Tetris
from BiblioPixelAnimations.game.flappy import Flappy
from BiblioPixelAnimations.game.Snake import Snake
pad = SerialGamePad()
# anim = Tetris(led, pad, evil=True)
anim = Snake(led, pad)
anim.run(fps=30)
