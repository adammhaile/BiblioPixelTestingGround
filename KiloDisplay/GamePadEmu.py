import bibliopixel.log as log
log.setLogLevel(log.logging.DEBUG)

import win32api
import win32con

from bibliopixel.util import d

class GamePadEmu():
    foundDevices = []
    def __init__(self, btn_map = [[win32con.VK_UP, "UP"], [win32con.VK_DOWN, "DOWN"], [win32con.VK_LEFT, "LEFT"], [win32con.VK_RIGHT, "RIGHT"], [win32con.VK_SPACE, "FIRE"], ["A","A"],["S","B"],["Z","X"],["X","Y"]]):
        self._map = btn_map

    def getKeys(self):
        result = {}
        for m in self._map:
            key = m
            val = m
            if isinstance(m, list):
                val = m[0]
                key = m[1]
            if isinstance(val, str):
                val = ord(val[0])

            result[key] = abs(win32api.GetAsyncKeyState(val)) > 1
        return d(result)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def setLights(self, data):
        pass

    def setLightsOff(self, count):
        pass
