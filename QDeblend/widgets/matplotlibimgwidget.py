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

import sys
import os
import random
import matplotlib
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from QDeblend.process import mask_def
import color_schema

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

__version__ = '0.1.2'


class MatplotlibImgWidget(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, name=None, width=4, height=4, dpi=100, bgcolor=None):
	self.parent = parent
#	if self.parent:
		#bgc = parent.backgroundBrush().color()
		#bgcolor = float(bgc.red())/255.0, float(bgc.green())/255.0, float(bgc.blue())/255.0
		#bgcolor = "#%02X%02X%02X" % (bgc.red(), bgc.green(), bgc.blue())
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=bgcolor, edgecolor=bgcolor)
        self.axes = self.fig.add_axes([0.05, 0.05, 0.9, 0.9])
        # We want the axes cleared every time plot() is called
        self.colorScheme = color_schema.colorSchemeSpax()
        self.axes.hold(False)
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.image = None
        self.pickRectangle= None
        self.selectSpaxMask = None
        self.limitsWidget = None
        self.zoomRect = None
        #self.axes.set_tickslabels([])
        
        
        
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
        
    def clearWidget(self):
        self.image=None
        self.selectSpaxMask = None
        self.pickRectangle = None
        self.axes.clear()
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.fig.canvas.draw()
        
    def setLimitsWidget(self, limits_widget):
        self.limitsWidget = limits_widget
        self.connect(self.limitsWidget, SIGNAL("limitsChanged"), self.setCLim)
     
        
    def initImage(self, image, limits=True):
        self.image = self.axes.imshow(image, interpolation=self.colorScheme.image['interpolation'], filterrad=self.colorScheme.image['radius'], origin = 'lower', cmap=matplotlib.cm.get_cmap(self.colorScheme.image['colormap']), zorder=1) 
        if self.limitsWidget.auto==True and limits==True:
            min = numpy.min(image)
            max = numpy.max(image) 
            self.limitsWidget.setLimits(min, max)
            if self.colorScheme.image['scaling']=='Logarithmic':
                if min<0:
                    vmin=1e-5
                else:
                    vmin=min
                norm = matplotlib.colors.LogNorm(vmin=vmin, vmax=max)
                self.image.set_norm(norm)
            else:
                self.image.set_clim(min, max)
        else:
            if self.colorScheme.image['scaling']=='Logarithmic':
                if self.limitsWidget.min<0:
                    vmin=1e-5
                else:
                    vmin=self.limitsWidget.min
                norm = matplotlib.colors.LogNorm(vmin=vmin, vmax=self.limitsWidget.max)
                self.image.set_norm(norm)
            else:
                self.image.set_clim(self.limitsWidget.min, self.limitsWidget.max)

        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.fig.canvas.draw()
        
    def initSpaxMask(self, visible):
        dim = self.image.get_array().shape
        if  self.colorScheme.select['hatch']!='None':
            fill = False
            hatch = self.colorScheme.select['hatch']
        else:
            fill= True
            hatch = None
        self.selectSpaxMask = mask_def.displayImgMask(self,  (dim[0], dim[1]),  hatch=hatch, color=self.colorScheme.select['color'], fill=fill, visible=visible)
        
    def setCLim(self, min, max):
        if self.colorScheme.image['scaling']=='Logarithmic':
            if min<0:
                vmin=1e-5
            else:
                vmin=min
            norm = matplotlib.colors.LogNorm(vmin=vmin, vmax=max)
            self.image.set_norm(norm)
        else:
            self.image.set_clim(min, max)
        self.fig.canvas.draw()
        
    def initShowSpax(self, x, y, visible):
        self.showSpax = [(x-0.5, y-0.5), visible]
        if  self.colorScheme.marker['hatch']!='None':
            fill = False
            hatch = self.colorScheme.marker['hatch']
        else:
            fill= True
            hatch = None
        self.pickRectangle = matplotlib.patches.Rectangle(xy=self.showSpax[0], width=1.0, height=1.0, lw=self.colorScheme.marker['width'],  ec=self.colorScheme.marker['color'], fc=self.colorScheme.marker['color'],fill=fill, visible=self.showSpax[1], hatch = hatch,  alpha=self.colorScheme.marker['alpha'], zorder=10)
        self.axes.add_artist(self.pickRectangle)
        self.fig.canvas.draw()
        
    def initZoomBox(self, x, y):
        self.xyZoom = (x, y)
        self.widthZoom = (0, 0)
        self.zoomRect = matplotlib.patches.Rectangle(xy=(x-0.5, y-0.5), width=0.0, height=0.0, ec='r',lw=1.5,  fill=False, visible=True, zorder=10)
        self.zoomArtist = self.axes.add_artist(self.zoomRect)
        self.fig.canvas.draw()
        
    def updateImage(self, image, limits=True):
        
        if self.limitsWidget.auto==True and limits==True:
            min = numpy.min(image)
            max = numpy.max(image) 
            if self.colorScheme.image['scaling']=='Logarithmic':
                if min<0:
                    vmin=1e-5
                else:
                    vmin=min
                norm = matplotlib.colors.LogNorm(vmin=vmin, vmax=max)
                self.image.set_norm(norm)
                self.image.set_data(image)
            else:
                self.image.set_data(image)
                self.image.set_clim(min,max)
            self.limitsWidget.setLimits(min, max)
        else:
            if self.colorScheme.image['scaling']=='Logarithmic':
                if self.limitsWidget.min<0:
                    vmin=1e-5
                else:
                    vmin=self.limitsWidget.min
                norm = matplotlib.colors.LogNorm(vmin=vmin,  vmax=self.limitsWidget.max)
                self.image.set_norm(norm)
            else:
                self.image.set_data(image)
                self.image.set_clim(self.limitsWidget.min,self.limitsWidget.max)
        self.fig.canvas.draw()
        
    def moveSelectSpax(self, x, y):
        self.showSpax = [(x-0.5, y-0.5), self.showSpax[1]]
        self.pickRectangle.set_xy((x, y))
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
        if self.image!=None:
            array = self.image.get_array()
            dim = array.shape
            self.axes.set_xlim(-0.5,dim[1]-1.5)  
            self.axes.set_ylim(-0.5,dim[0]-1.5)  
            self.fig.canvas.draw()


    def updateColorScheme(self):
        if self.image!=None:
            if self.colorScheme.image['reversed']:
                cmap = self.colorScheme.image['colormap']+'_r'
            else:
                cmap = self.colorScheme.image['colormap']
            self.image.set_cmap(matplotlib.cm.get_cmap(cmap))
            self.image.set_interpolation(self.colorScheme.image['interpolation'])
            self.image.set_filterrad(self.colorScheme.image['radius'])
            if self.colorScheme.image['scaling']=='Linear':
                norm = matplotlib.colors.NoNorm()
                self.image.set_norm(norm)
                self.image.set_clim(self.limitsWidget.min,self.limitsWidget.max)
            elif self.colorScheme.image['scaling']=='Logarithmic':
                if self.limitsWidget.min<0:
                    vmin=1e-5
                else:
                    vmin=self.limitsWidget.min
                norm = matplotlib.colors.LogNorm(vmin=vmin, vmax=self.limitsWidget.max)
                self.image.set_norm(norm)
        if self.pickRectangle!=None:
            if  self.colorScheme.marker['hatch']!='None':
                self.pickRectangle.set_fill(False)    
                self.pickRectangle.set_hatch(self.colorScheme.marker['hatch'])
            else:
                self.pickRectangle.set_fill(True)    
                self.pickRectangle.set_hatch(None)
            self.pickRectangle.set_ec(self.colorScheme.marker['color'])
            self.pickRectangle.set_fc(self.colorScheme.marker['color'])
            self.pickRectangle.set_alpha(self.colorScheme.marker['alpha'])
            self.pickRectangle.set_lw(self.colorScheme.marker['width'])
        if self.selectSpaxMask!=None:
            if  self.colorScheme.select['hatch']!='None':
                self.selectSpaxMask.setFill(False)
                self.selectSpaxMask.setHatch(self.colorScheme.select['hatch'])
            else:
                self.selectSpaxMask.setFill(True)
                self.selectSpaxMask.setHatch(None)
            self.selectSpaxMask.setColor(self.colorScheme.select['color'])
            self.selectSpaxMask.setAlpha(self.colorScheme.select['alpha'])
        self.fig.canvas.draw()
        
    
    
    
    def onclick(self,event):
        self.emit(SIGNAL("mouse_press_event"),event.button,event.x,event.y,event.xdata,event.ydata)
 #       print 'button=%d, x=%d, y=%d, xdata=%s, ydata=%s'%(
  #      event.button, event.x, event.y, str(event.xdata), str(event.ydata))

    def move(self,event):
        self.emit(SIGNAL("mouse_move_event"),event.button,event.x,event.y,event.xdata,event.ydata)
    
    def release(self, event):
        self.emit(SIGNAL("mouse_release_event"),event.button,event.x,event.y,event.xdata,event.ydata)

    def sizeHint(self):
        w = self.fig.get_figwidth()
        h = self.fig.get_figheight()
        return QSize(w, h)

    def minimumSizeHint(self):
        return QSize(10, 10)

        
    
