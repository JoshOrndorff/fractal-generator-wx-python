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
    self.txtVerticies = VertextCtrl(self, pos=(30, 290), size=(250, 150))
    
    # Points field
    wx.StaticText(self, label="Points:", pos=(320, 320))
    self.txtPoints = wx.TextCtrl(self, pos=(380, 300), size=(200, 50))
    self.txtPoints.SetValue("100")
    #TODO Advanced option: manually choose the original point
    
    # Generate Button
    btnGenerate = wx.Button(self, label="Generate", pos=(400, 380))
    btnGenerate.Bind(wx.EVT_BUTTON, self.OnGenerate)
    
    # Make the window appear
    self.Centre()
    self.Show()
  
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
      vertex = choice(self.txtVerticies.verticies)
      
      # Calculate the midpoint between them
      newPoint = ((self.points[-1][0] + vertex[0]) / 2, (self.points[-1][1] + vertex[1]) / 2)
      self.points.append(newPoint)
      
    self.panel.Refresh(self.txtVerticies.verticies, self.points)
      
      
class VertextCtrl(wx.TextCtrl):
  def __init__(self, *args, **kwargs):
    super(VertextCtrl, self).__init__(*args, style = wx.TE_MULTILINE | wx.TE_RICH, **kwargs)
    
    self.SetValue("20, 40\n70, 20\n50, 86")
    
    self.Bind(wx.EVT_KILL_FOCUS, self.OnVerticiesEntered)
    self.OnVerticiesEntered(None)
    
  def OnVerticiesEntered(self, e):
    self.verticies = []
    x = 0
    y = 0
    
    readText = self.GetValue().split('\n')
    self.SetValue('')
    
    for line in readText:
      if line.count(',') != 1:
        # Not exactly one comma, make line red
        self.SetForegroundColour(wx.RED)
      try:
        x = float(line.split(',')[0].strip())
        y = float(line.split(',')[1].strip())
      except ValueError:
        # Not numbers, make line red
        self.SetForegroundColour(wx.RED)
      if x > 100 or y > 100 or x < 0 or y < 0:
        # Numbers not in proper range, make line red
        self.SetForegroundColour(wx.RED)
      
      # If the line isn't blank, write it back to the TextCtrl
      if line.strip() != '':
        self.AppendText(line + '\n')
        
      # Default the cursor to black for next time
      self.SetForegroundColour(wx.BLACK)
      
      # If converted, append it to the list of verticies
      self.verticies.append((x / 100.0, y / 100.0))
      

    
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
  
  #TODO Should this panel have its own copy of the verticies and points that are currently displayed for things like resizing?
  # Yes. It occurs when I resize the window to cover part of the panel, then make it bigger again.
  # But still, it doesn't need to be redrawn every time the frame is redrawn.
  
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
