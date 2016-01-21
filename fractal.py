#!/usr/bin/python

import wx
from random import choice, random

class FractalFrame(wx.Frame):
  def __init__(self, title):
    super(FractalFrame, self).__init__(None, title=title, size=(600, 500))
    
    self.verticies = []
    self.points = []
    
    # Set up the frame icon (http://www.programmingforums.org/thread15370.html)
    #favicon = wx.Icon('favicon.ico', wx.BITMAP_TYPE_ICO, 16, 16)
    #self.SetIcon(favicon)
    
    #TODO Make sizers after the main code works
    
    # The panel for drawing
    self.panel = FractalPanel(self, pos=(10,10), size=(580, 250))
    
    # The list of verticies
    wx.StaticText(self, label="Verticies:", pos=(30, 270))
    self.txtVerticies = wx.TextCtrl(self, pos=(30, 290), size=(250, 150), style=wx.TE_MULTILINE | wx.TE_RICH)
    self.txtVerticies.Bind(wx.EVT_KILL_FOCUS, self.OnVerticiesEntered)
    self.txtVerticies.SetValue("20, 40\n70, 20\n50, 86")
    self.OnVerticiesEntered(None)
    
    # Points field
    wx.StaticText(self, label="Points:", pos=(320, 320))
    self.txtPoints = wx.TextCtrl(self, pos=(380, 300), size=(200, 50))
    self.txtPoints.SetValue("100")
    #TODO Advanced option: manually choose the original point
    
    # Generate Button
    btnGenerate = wx.Button(self, label="Generate", pos=(400, 380))
    btnGenerate.Bind(wx.EVT_BUTTON, self.OnGenerate)
    
    # Pass repaint events along to the panel
    self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    # Make the window appear
    self.Centre()
    self.Show()
    
  def OnVerticiesEntered(self, e):
    #TODO Make it red when they are no good: http://stackoverflow.com/questions/8588287/wxpython-how-to-change-the-font-color-in-textctrl-with-a-checkbox
    
    self.verticies = []
    x = 0
    y = 0
    
    readText = self.txtVerticies.GetValue().split('\n')
    self.txtVerticies.SetValue('')
    
    for line in readText:
      if line.count(',') != 1:
        # Not exactly one comma, make line red
        self.txtVerticies.SetForegroundColour(wx.RED)
      try:
        x = float(line.split(',')[0].strip())
        y = float(line.split(',')[1].strip())
      except ValueError:
        # Not numbers, make line red
        self.txtVerticies.SetForegroundColour(wx.RED)
      if x > 100 or y > 100 or x < 0 or y < 0:
        # Numbers not in proper range, make line red
        self.txtVerticies.SetForegroundColour(wx.RED)
      
      # If the line isn't blank, write it back to the TextCtrl
      if line.strip() != '':
        self.txtVerticies.AppendText(line + '\n')
        
      # Default the cursor to black for next time
      self.txtVerticies.SetForegroundColour(wx.BLACK)
      
      # If converted, append it to the list of verticies
      self.verticies.append((x / 100.0, y / 100.0))
    
  def OnPaint(self, e):
    self.panel.Refresh(self.verticies, self.points)
  
  def OnGenerate(self, e):
    
    # Reset points and choose a random first point
    self.points = []
    self.points.append((random(), random()))
    
    #TODO Use a slider for number of points
    try:
      numPoints = int(float(self.txtPoints.GetValue()))
      self.txtPoints.SetValue(str(numPoints))
      
    except ValueError:
      print("Number of points must be an int.") #TODO Better error checking
    
    # Calculate each subsequent point
    while len(self.points) < numPoints:
      # Choose a random vertex
      vertex = choice(self.verticies)
      
      # Calculate the midpoint between them
      newPoint = ((self.points[-1][0] + vertex[0]) / 2, (self.points[-1][1] + vertex[1]) / 2)
      self.points.append(newPoint)
      
    self.panel.Refresh(self.verticies, self.points)
      
      
      

    
class FractalPanel(wx.Panel):
  def __init__(self, *args, **kwargs):
    super(FractalPanel, self).__init__(*args, **kwargs)
    
    # Set the circle radius
    self.vertexSize = 5
    self.pointSize  = 3
    
    # Make background green
    self.SetBackgroundColour('GREEN')
    
    # Setup pens for verticies and points
    self.vbrush = wx.Brush('BLUE')
    self.pbrush = wx.Brush('WHITE')
  
  def Refresh(self, verticies, points):
    dc = wx.PaintDC(self)
    dc.Clear()
    
    w, h = self.GetSizeTuple()
    
    # Draw the verticies
    dc.SetBrush(self.vbrush)
    for vertex in verticies:
      dc.DrawCircle(vertex[0] * w, vertex[1] * h, self.vertexSize) #TODO Why can this not be done with a point object?
    
    # Draw the points
    dc.SetBrush(self.pbrush)
    for point in points:
      dc.DrawCircle(point[0] * w, point[1] * h, self.pointSize)

if __name__ == '__main__':
  app = wx.App()
  FractalFrame("Brad's Fractal Demonstration")
  app.MainLoop()
