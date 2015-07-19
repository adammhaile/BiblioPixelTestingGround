import wx
import time
import threading

import os
#os.sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#import log

from bibliopixel import *

from bibliopixel.drivers.network_receiver import ThreadedDataServer, ThreadedDataHandler

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

# Thread class that executes processing
class WorkerThread(threading.Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        """Run Worker Thread."""
        colors = [(255,0,0), (0,255,0), (0,0,255)]
        while True:
            for i in range(len(colors)):
                time.sleep(0.1)
                if self._want_abort:
                    wx.PostEvent(self._notify_window, ResultEvent(None))
                    return
                else:
                    wx.PostEvent(self._notify_window, ResultEvent(colors[i]))

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1

class View(wx.Panel):
    def __init__(self, parent, size):
        super(View, self).__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        w, h = self.GetClientSize()
        self.x = 20 
        self.y = 50
        self.data = [0]*(self.x*self.y*3)
        self._hasFrame = False

        # Set up event handler for any worker thread results
        EVT_RESULT(self,self.OnResult)

        #self.worker = WorkerThread(self)

        address = ('localhost', 1618)
        try:
            server = ThreadedDataServer(address, ThreadedDataHandler)
            server.update = self.update
            server.hasFrame = self.hasFrame

            t = threading.Thread(target=server.serve_forever)
            t.setDaemon(True) # don't hang on exit
            t.start()
        except Exception as e:
            log.logger.exception(e)
            log.logger.error("Unable to open port. Another visualizer is likely running. Exiting...")
            sys.exit(2)

    def on_size(self, event):
        event.Skip()
        self.Refresh()
    def on_paint(self, event):
        w, h = self.GetClientSize()
        dc = wx.AutoBufferedPaintDC(self)
        pw = w / self.x
        ph = pw

        dc.Clear()
        dc.SetPen(wx.Pen(wx.Colour(16,16,16), 1))
        data = self.data
        for x in range(self.x):
            for y in range(self.y):
                i = x+(y*self.x)
                r = data[i * 3 + 0]
                g = data[i * 3 + 1]
                b = data[i * 3 + 2]
                
                dc.SetBrush(wx.Brush(wx.Colour(r,g,b)))
                dc.DrawRectangle(x*pw, y*ph, pw, ph)

        self._hasFrame = False

    def update(self, data):
        wx.PostEvent(self, ResultEvent(data))

    def hasFrame(self):
    	return self._hasFrame

    def OnResult(self, event):
        self.data = event.data
        self._hasFrame = True
        self.Refresh()
        self.Update()


class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None)
        self.SetTitle('Visualizer')
        self.SetClientSize((500, 500))
        self.Center()
        self.view = View(self, (500, 500))

def main():
    app = wx.App(False)
    frame = Frame()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()