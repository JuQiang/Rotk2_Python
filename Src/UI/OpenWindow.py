import wx
from Src.UI.Draw import Draw
import sched
import datetime
import time

class OpenWindow(wx.Dialog):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, '', style=wx.CLOSE_BOX | wx.BORDER_NONE)
        self.SetInitialSize(wx.Size(640, 400))
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.splash_index = 1

        self.loop_monitor()

        self.Centre()
        self.Show()

    def loop_monitor(self):
        s = sched.scheduler(time.time, time.sleep)  # 生成调度器

        s.enter(2, 1, self.InvalidateSplashScreen, ())
        s.run()

    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        brush = wx.Brush("black")
        dc.SetBackground(brush)
        dc.Clear()

        splash = Draw().GetSplashScreen("logo{0}".format(self.splash_index))
        dc.DrawBitmap(splash,0,0)

    def InvalidateSplashScreen(self):
        if self.splash_index>11:
            self.splash_index = 1
        self.Refresh()
        self.splash_index += 1
        print(self.splash_index)
