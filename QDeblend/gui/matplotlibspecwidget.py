# Copyright 2011 Bernd Husemann
#
#
#This file is part of QDeblend3D.
#
#QDeblend3D is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License  as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.
#
#QDeblend3D  is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with QDeblend3D.  If not, see <http://www.gnu.org/licenses/>.

import sys, os, random
import numpy
import mask_def
import own_classes
import matplotlib
from PyQt4.QtCore import *
from PyQt4.QtGui import *


from numpy import arange, sin, pi

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

__version__ = '0.1.2'


class MatplotlibSpecWidget(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, name=None, width=4, height=4, dpi=80, bgcolor=None):
	self.parent = parent
#	if self.parent:
		#bgc = parent.backgroundBrush().color()
		#bgcolor = float(bgc.red())/255.0, float(bgc.green())/255.0, float(bgc.blue())/255.0
		#bgcolor = "#%02X%02X%02X" % (bgc.red(), bgc.green(), bgc.blue())
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=bgcolor, edgecolor=bgcolor)
        self.axes = self.fig.add_axes([0.07, 0.12, 0.91, 0.86])
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        #self.axes.set_xticklabels(self.axes.get_xticklabels(), fontsize=10)
        self.axes.set_xlabel('wavelength [$\AA$]',  fontsize=12)
        self.colorScheme = own_classes.colorSchemeSpec()
        self.spec1_vis = False
        self.spec2_vis = False
        self.viewLine_vis = False
        self.spec1 = None
        self.spec2 = None
        self.viewLine = None
        self.limitsWidget = None
        self.selectSpecMask = None
        self.xlim = [0, 0]
        
        FigureCanvas.__init__(self, self.fig)
##        self.reparent(parent, QPoint(0, 0))

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.cid=self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.cid2=self.fig.canvas.mpl_connect('motion_notify_event', self.move)
        self.cid3=self.fig.canvas.mpl_connect('button_release_event', self.release)
        self.connect(self.colorScheme, SIGNAL("changed()"), self.updateColorScheme)
 #       self.cid4=self.fig.canvas.mpl_connect('pick_event', self.onpick)
 
    def clearWidget(self):
        self.spec1 = None
        self.spec1 = None
        self.spec2 = None
        self.viewLine = None
        self.selectSpecMask = None
        self.spec1_vis = False
        self.spec2_vis = False
        self.viewLine_vis = False
        self.xlim = [0, 0]
        self.axes.clear()
        self.axes.set_xlabel('wavelength [$\AA$]',  fontsize=12)
        self.fig.canvas.draw()
        
    def setLimitsWidget(self, limits_widget):
        self.limitsWidget = limits_widget
        self.connect(self.limitsWidget, SIGNAL("limitsChanged"), self.setYLim)
        
    def initSpec1(self, wave, spec1):
        self.spec1 = self.axes.add_line(matplotlib.lines.Line2D(wave, spec1, linestyle=self.colorScheme.spec1['style'], color=self.colorScheme.spec1['color'], lw=self.colorScheme.spec1['width']))
        self.spec1_vis = True
        
        if self.limitsWidget.auto==True:
            min = numpy.min(spec1)
            max = numpy.max(spec1) 
            self.axes.set_ylim(min,max)
            self.limitsWidget.setLimits(min, max)
        else:
            self.axes.set_ylim(self.limitsWidget.min,self.limitsWidget.max)
        self.fig.canvas.draw()
        
    def initSpec2(self, wave, spec2):
        self.spec2 = self.axes.add_line(matplotlib.lines.Line2D(wave, numpy.zeros(wave.shape[0]), linestyle=self.colorScheme.spec2['style'], color=self.colorScheme.spec2['color'], lw=self.colorScheme.spec2['width']))
        self.spec2_vis = True
        if self.limitsWidget.auto==True:
            min = numpy.min(spec2)
            max = numpy.max(spec2) 
            self.axes.set_ylim(min,max)
            self.limitsWidget.setLimits(min, max)
        else:
            self.axes.set_ylim(self.limitsWidget.min,self.limitsWidget.max)
        self.fig.canvas.draw()
        
    def initViewLine(self, wave):
        self.viewLine = self.axes.axvline(wave, linestyle=self.colorScheme.slicer['style'], color=self.colorScheme.slicer['color'], lw=self.colorScheme.slicer['width'])
        self.viewLine_vis = True
        self.fig.canvas.draw()
        
    def initZoomBox(self, x, y):
        self.xyZoom = (x, y)
        self.zoomRect = matplotlib.patches.Rectangle(xy=(x, y), width=0.0, height=0.0,  ec=self.colorScheme.zoom['color'], lw=self.colorScheme.zoom['width'],  fill=False, visible=True, zorder=10)
        self.zoomArtist = self.axes.add_artist(self.zoomRect)
        self.widthZoom = (0, 0)
        self.fig.canvas.draw()
        
    def initSpecMask(self, waveLimit=None, visible=False):
        self.selectSpecMask = mask_def.displaySpecRegion(self, waveLimit=waveLimit, linestyle=self.colorScheme.select['style'], color=self.colorScheme.select['color'], lw=self.colorScheme.select['width'], hatch=self.colorScheme.select['hatch'], fill=False, visible=visible, alpha=self.colorScheme.select['alpha'])
        if  self.colorScheme.select['hatch']==None:
            self.selectSpecMask.setFill(True)
        self.changeSelectSpec = False
        
    def setXLim(self, xlim):
        self.xlim = xlim
        self.axes.set_xlim(xlim)
        self.fig.canvas.draw()
#    def updateViewLine(self, pos):

    def setYLim(self, ymin, ymax):
        self.axes.set_ylim((ymin, ymax))
        self.fig.canvas.draw()
 
    def updateSpec1(self, wave, spec1, limits=True):
        self.spec1.set_data(wave, spec1)
        self.spec1.set_visible(True)
        self.spec1_vis = True
        if self.limitsWidget.auto==True and limits:
            min = numpy.min(spec1)
            max = numpy.max(spec1) 
            self.axes.set_ylim(min,max)
            self.limitsWidget.setLimits(min, max)
        else:
            self.axes.set_ylim(self.limitsWidget.min,self.limitsWidget.max)
        self.fig.canvas.draw()
        
    def updateSpec2(self, wave, spec2, limits=True):
        self.spec2.set_data(wave, spec2)
        self.spec2.set_visible(True)
        self.spec2_vis = True
        if self.limitsWidget.auto==True and limits:
            min = numpy.min(spec2)
            max = numpy.max(spec2) 
            self.axes.set_ylim(min,max)
            self.limitsWidget.setLimits(min, max)
        else:
            self.axes.set_ylim(self.limitsWidget.min,self.limitsWidget.max)
        self.fig.canvas.draw()
        
    def setVisibleSpec2(self, visible):
        self.spec2.set_visible(visible)
        self.spec2_vis = visible
        self.fig.canvas.draw()
        
    def setVisibleSpec1(self, visible):
        self.spec1.set_visible(visible)
        self.spec1_vis = visible
        self.fig.canvas.draw()
    
        
    def updateViewLine(self, wave):
        self.viewLine.set_data([wave, wave], [0, 1])
        self.fig.canvas.draw()
        
    def resizeZoomBox(self, x, y):
        self.widthZoom = (x-self.xyZoom[0], y-self.xyZoom[1])
        self.zoomRect.set_width(x-self.xyZoom[0])
        self.zoomRect.set_height(y-self.xyZoom[1])
        self.fig.canvas.draw()
        
    def getZoomLimit(self):
        if self.widthZoom != (0, 0):
            xmin = numpy.min([self.xyZoom[0], self.xyZoom[0]+self.widthZoom[0]])
            xmax = numpy.max([self.xyZoom[0], self.xyZoom[0]+self.widthZoom[0]])
            ymin = numpy.min([self.xyZoom[1], self.xyZoom[1]+self.widthZoom[1]])
            ymax = numpy.max([self.xyZoom[1], self.xyZoom[1]+self.widthZoom[1]])
            return xmin, xmax, ymin, ymax
        else:
            return None
            
    def delZoomBox(self):
        self.zoomArtist.remove()
        self.zoomRect = None
        self.widthZoom = None
        self.xyZoom = None
        self.fig.canvas.draw()
        
    def zoomOut(self):
        if self.spec1!=None:
            spec= self.spec1.get_data(orig=True)
            self.axes.set_xlim(spec[0][0],spec[0][-1])  
            self.axes.set_ylim(numpy.min(spec[1]),numpy.max(spec[1]))  
            self.fig.canvas.draw()
            
    def updateColorScheme(self):
        if self.spec1!=None:
            self.spec1.set_color(self.colorScheme.spec1['color'])
            self.spec1.set_linewidth(self.colorScheme.spec1['width'])
            self.spec1.set_linestyle(self.colorScheme.spec1['style'])
        if self.spec2!=None:
            self.spec2.set_color(self.colorScheme.spec2['color'])
            self.spec2.set_linewidth(self.colorScheme.spec2['width'])
            self.spec2.set_linestyle(self.colorScheme.spec2['style'])
        if self.viewLine!=None:
            self.viewLine.set_color(self.colorScheme.slicer['color'])
            self.viewLine.set_linewidth(self.colorScheme.slicer['width'])
            self.viewLine.set_linestyle(self.colorScheme.slicer['style'])
        if self.selectSpecMask!=None:
            self.selectSpecMask.setColor(self.colorScheme.select['color'])
            self.selectSpecMask.setLineWidth(self.colorScheme.select['width'])
            self.selectSpecMask.setLineStyle(self.colorScheme.select['style'])
            self.selectSpecMask.setAlpha(self.colorScheme.select['alpha'])
            self.selectSpecMask.setHatch(self.colorScheme.select['hatch'])
            if self.colorScheme.select['hatch']==None:
                self.selectSpecMask.setFill(True)
            else:
                self.selectSpecMask.setFill(False)
        self.fig.canvas.draw()
 #   def setVisible(self, spec1_vis = None, spec2_vis = None, viewLine_vis = None):
  #      if spec1_vis !=None:
   #         self.spec1_vis = spec1_vis
    #        self.spec1[0].set_visible(self.spec1_vis)
            
    #    if spec2_vis !=None:
     #       self.spec2_vis = spec2_vis
      #      self.spec2[0].set_visible(self.spec2_vis)
       # if viewLine_vis !=None:
        #    self.viewLine_vis = viewLine_vis
         #   self.viewLine.set_visible(self.viewLine_vis)
        #self.fig.canvas.draw()
        
    def onclick(self,event):
        self.emit(SIGNAL("mouse_press_event"),event.button,event.x,event.y,event.xdata,event.ydata)
#        print 'button=%d, x=%d, y=%d, xdata=%s, ydata=%s'%(
#        event.button, event.x, event.y, str(event.xdata), str(event.ydata))

    def move(self,event):
        self.emit(SIGNAL("mouse_move_event"),event.button,event.x,event.y,event.xdata,event.ydata)
        
    def release(self, event):
        self.emit(SIGNAL("mouse_release_event"),event.button,event.x,event.y,event.xdata,event.ydata)

    def onpick(self, event):
        thisline = event.artist     
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        print thisline, ind
        print 'onpick points:', zip(xdata[ind], ydata[ind])




    def sizeHint(self):
        w = self.fig.get_figwidth()
        h = self.fig.get_figheight()
        return QSize(w, h)

    def minimumSizeHint(self):
        return QSize(10, 10)


 
