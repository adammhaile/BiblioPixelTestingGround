from GamePadEmu import GamePadEmu
from SerialGamePad import SerialGamePad

pad = None
try:
    pad = SerialGamePad()
except:
    pad = GamePadEmu()
