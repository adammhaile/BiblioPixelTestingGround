import win32api
import win32con
import time

while True:
    state =  win32api.GetAsyncKeyState(ord('H'))
    print abs(state) > 1
    time.sleep(1)
