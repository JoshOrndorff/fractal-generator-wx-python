#!/usr/bin/python

import wx
from random import choice, randint
from re import match

class FractalFrame(wx.Frame):
  def __init__(self, title):
    super(FractalFrame, self).__init__(None, title=title, size=(600, 500))
    
    # Set up the frame icon (http://www.programmingforums.org/thread15370.html)
    #favicon = wx.Icon('favicon.ico', wx.BITMAP_TYPE_ICO, 16, 16)
    #self.SetIcon(favicon)
    
    #TODO Make sizers after the main code works
    
    # The panel for drawing
    self.panel = FractalPanel(self, pos=(10,10), size=(580, 250))
    
    # The list of verticies
    wx.StaticText(self, label="Verticies:", pos=(30, 270))
    self.txtVerticies = wx.TextCtrl(self, pos=(30, 290), size=(250, 150), style=wx.TE_MULTILINE)
    self.txtVerticies.SetValue("200, 40\n300, 200\n500, 100")
    
    # Points field
    wx.StaticText(self, label="Points:", pos=(320, 320))
    self.txtPoints = wx.TextCtrl(self, pos=(380, 300), size=(200, 50))
    self.txtPoints.SetValue("100")
    #TODO Advanced option: manually choose the original point
    
    # Generate Button
    btnGenerate = wx.Button(self, label="Generate", pos=(400, 380))
    btnGenerate.Bind(wx.EVT_BUTTON, self.OnGenerate)
    
    # The computation variables
    self.points = []
    self.verticies = []
    
    # Pass repaint events along to the panel
    self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    # Make the window appear
    self.Centre()
    self.Show()
    
  def OnPaint(self, e):
    self.panel.Refresh(self.verticies, self.points)
  
  def OnGenerate(self, e):
    # Retrieve the verticies
    self.verticies = []
    
    #TODO Make sure the point data is valid. I'm starting to think there is a better control to use.
    # Or maybe I should validate that data as soon as the textchanged event happens?
    for line in self.txtVerticies.GetValue().split('\n'):
      x = int(line.split(',')[0].strip())
      y = int(line.split(',')[1].strip())
      
      # If converted, append it to the list of verticies
      self.verticies.append(wx.Point(x, y))
      
      #TODO Or if not, inform the user by one of the following methods:
      #Message Box, Static Text, Turning the invalid item(s) red. That's a good one.
    
    
    # Reset points and choose a random first point
    self.points = []
    self.points.append(wx.Point(randint(0, 100), randint(0, 100)))
    
    #TODO Use a slider for number of points
    try:
      numPoints = int(float(self.txtPoints.GetValue()))
      self.txtPoints.SetValue(str(numPoints))
      
    except ValueError:
      print("Number of points must be an int.") #TODO Better error checking
    
    # Calculate each subsequent point
    while len(self.points) < numPoints:
      #Choose a random vertex
      vertex = choice(self.verticies)
      
      # Calculate the midpoint between them
      newPoint = wx.Point((self.points[-1].x + vertex.x) / 2, (self.points[-1].y + vertex.y) / 2)
      self.points.append(newPoint)
      
    self.panel.Refresh(self.verticies, self.points)
      
      
      

    
class FractalPanel(wx.Panel):
  def __init__(self, *args, **kwargs):
    wx.Panel.__init__(self, *args, **kwargs) #TODO Why does super not seem to work here?
    
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
    
    # Draw the verticies
    dc.SetBrush(self.vbrush)
    for vertex in verticies:
      dc.DrawCircle(vertex.x, vertex.y, self.vertexSize) #TODO Why can this not be done with a point object?
    
    # Draw the points
    dc.SetBrush(self.pbrush)
    for point in points:
      dc.DrawCircle(point.x, point.y, self.pointSize)

if __name__ == '__main__':
  app = wx.App()
  FractalFrame("Brad's Fractal Demonstration")
  app.MainLoop()
