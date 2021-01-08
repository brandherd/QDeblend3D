import numpy
import matplotlib
from QDeblend.process.exceptions import UnfilledMaskError

class mask(object):
    def __init__(self,dim,init_mask_array=None):
        self.mask = numpy.zeros(dim, dtype=numpy.bool)
        self.dim = dim
        if init_mask_array is not None and self.dim == init_mask_array.shape:
            self.mask =init_mask_array
            
    def maskPixel(self, position):
        self.mask[tuple(position)] = True
    
    def unmaskPixel(self, position):
        self.mask[tuple(position)] = False
    
    def isMaksed(self, position):
        return self.mask[tuple(position)] 
        
    def maskedPixel(self):
        return numpy.sum(self.mask.flatten())
    
    def maskBox(self, center, boxsize):
        if (boxsize-1)%2 == 0 and center[0]-(boxsize-1)//2>=0 and center[0]+(boxsize-1)//2+1<=self.dim[0] and \
                center[1]-(boxsize-1)//2>=0 and center[1]+(boxsize-1)//2+1<=self.dim[1]:
            self.mask[int(center[0]-(boxsize-1)//2):int(center[0]+(boxsize-1)//2+1),
            int(center[1]-(boxsize-1)//2):int(center[1]+(boxsize-1)//2+1)] = True
    
    def unmaskBox(self, center, boxsize):
        if (boxsize-1)%2 == 0 and center[0]-(boxsize-1)//2>=0 and center[0]+(boxsize-1)//2+1<=self.dim[0] and \
                center[1]-(boxsize-1)//2>=0 and center[1]+(boxsize-1)//2+1<=self.dim[1]:
            self.mask[int(center[0]-(boxsize-1)//2):int(center[0]+(boxsize-1)//2+1),
            int(center[1]-(boxsize-1)//2):int(center[1]+(boxsize-1)//2+1)] = False
    
    def maskShell(self, center, boxsize, width):
        self.maskBox( center, boxsize + 2 * width)
        self.unmaskBox(center, boxsize)


class displayImgMask(mask):
    def __init__(self, canvas,  dim, init_mask_array=None, visible=False, hatch=None, fill=True,
                 lw=1.0, color='0.7',zorder=3, alpha=0.5):
        if len(dim)==2:
            self.mask = mask(dim, init_mask_array)
            self.map = numpy.zeros(dim, dtype=numpy.int32)
            self.area = []
            self.dim = dim
            self.masked = 1
            self.visible = visible
            self.alpha = alpha
            self.color = color
            self.fill = fill
            self.lw = lw
            self.hatch = hatch
            self.zorder = zorder
            self.canvas = canvas
            if init_mask_array is not None:
                for i in range(dim[0]):
                    for j in range(dim[1]):
                        if self.mask.mask[i, j]==True:
                            self.area.append(matplotlib.patches.Rectangle(xy=(j-0.5, i-0.5), width=1.0, height=1.0,
                                                                          color=color, lw=lw, ec=color, fc=color,
                                                                          fill=fill, visible=visible, hatch=hatch,
                                                                          zorder=zorder, alpha=alpha))
                            self.map[(i, j)] = self.masked
                            self.canvas.axes.add_artist(self.area[self.masked - 1])
                            self.masked += 1
                self.canvas.fig.canvas.draw()

    def maskArray(self, array):
        self.emptyMask()
        array = numpy.array(array)
        dim = array.shape
        self.mask = mask(dim, array)
        for i in range(dim[0]):
            for j in range(dim[1]):
                if self.mask.mask[i, j]==True:
                    self.area.append(matplotlib.patches.Rectangle(xy=(j-0.5, i-0.5), width=1.0, height=1.0,
                                                                  color=self.color, lw=self.lw, ec=self.color,
                                                                  fc=self.color,fill=self.fill, visible=self.visible,
                                                                  hatch=self.hatch, zorder=self.zorder,
                                                                  alpha=self.alpha))
                    self.map[(i, j)] = self.masked
                    self.canvas.axes.add_artist(self.area[self.masked-1])
                    self.masked += 1
        self.canvas.fig.canvas.draw()

    def maskPixel(self, position):
            self.mask.mask[tuple(position)] = True
            self.map[tuple(position)] = self.masked
            self.area.append(matplotlib.patches.Rectangle(xy=(position[1]-0.5, position[0]-0.5), width=1.0, height=1.0,
                                                          color=self.color, ec=self.color, fc=self.color,fill=self.fill,
                                                          hatch=self.hatch, visible=self.visible, zorder=self.zorder,
                                                          alpha=self.alpha))
            self.canvas.axes.add_artist(self.area[self.masked - 1])
            self.masked+=1
            self.canvas.fig.canvas.draw()
            
    def unmaskPixel(self, position):
            self.mask.mask[tuple(position)] = False
            self.area[self.map[tuple(position)] - 1].remove()
            del self.area[self.map[tuple(position)] - 1]
            self.map[self.map>self.map[tuple(position)] - 1] = self.map[self.map>self.map[tuple(position)] - 1] - 1
            self.map[tuple(position)] = 0
            self.masked -= 1
            self.canvas.fig.canvas.draw()
            
    def isMasked(self, position):
        return self.mask.mask[tuple(position)] 
        
    def maskedPixels(self):
        return self.masked
        
    def getMask(self):
        if not self.isEmpty():
            return self.mask.mask
        else:
            raise UnfilledMaskError
        
    def emptyMask(self):
        self.mask.mask= numpy.zeros(self.dim, dtype=numpy.bool)
        self.map = numpy.zeros(self.dim, dtype=numpy.int32)
        for i in range(len(self.area)):
            self.area[i].remove()
        self.area = []
        self.masked = 1
        self.canvas.fig.canvas.draw()
        
    def setMask(self, mask):
        self.emptyMask()
        self.mask.mask = mask
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                if self.mask.mask[i, j]==True:
                    self.area.append(matplotlib.patches.Rectangle(xy=(j-0.5, i-0.5), width=1.0, height=1.0,
                                                                  color=self.color, ec=self.color, fc=self.color,
                                                                  fill=self.fill, visible=self.visible,
                                                                  hatch=self.hatch, zorder=self.zorder,
                                                                  alpha=self.alpha))
                    self.map[(i, j)] = self.masked
                    self.canvas.axes.add_artist(self.area[self.masked - 1])
                    self.masked += 1
        self.canvas.fig.canvas.draw()

    def maskBox(self, center, boxsize):
        self.emptyMask()
        self.mask.maskBox(center, boxsize)
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                if self.mask.mask[i, j]==True:
                    self.area.append(matplotlib.patches.Rectangle(xy=(j-0.5, i-0.5), width=1.0, height=1.0,
                                                                  color=self.color, ec=self.color, fc=self.color,
                                                                  fill=self.fill, visible=self.visible,
                                                                  hatch=self.hatch, zorder=self.zorder,
                                                                  alpha=self.alpha))
                    self.map[(i, j)] = self.masked
                    self.canvas.axes.add_artist(self.area[self.masked - 1])
                    self.masked += 1
        self.canvas.fig.canvas.draw()
        
    def maskShell(self, center, boxsize, width):
        self.emptyMask()
        self.mask.maskShell(center, boxsize, width)
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                if self.mask.mask[i, j]==True:
                    self.area.append(matplotlib.patches.Rectangle(xy=(j-0.5, i-0.5), width=1.0, height=1.0,
                                                                  color=self.color, ec=self.color, fc=self.color,
                                                                  fill=self.fill, visible=self.visible,
                                                                  hatch=self.hatch, zorder=self.zorder,
                                                                  alpha=self.alpha))
                    self.map[(i, j)] = self.masked
                    self.canvas.axes.add_artist(self.area[self.masked- 1 ])
                    self.masked += 1
        self.canvas.fig.canvas.draw()
        
    def setVisible(self, visible):
            self.visible = visible
            if self.area!=[]:
                for i in range(len(self.area)):
                    self.area[i].set_visible(self.visible)
                self.canvas.fig.canvas.draw()
            
    def setAlpha(self, alpha):
        self.alpha = alpha
        if self.area!=[]:
            for i in range(len(self.area)):
                self.area[i].set_alpha(self.alpha)
        self.canvas.fig.canvas.draw()
        
    def setHatch(self, hatch):
        self.hatch = hatch
        if self.area!=[]:
            for i in range(len(self.area)):
                self.area[i].set_hatch(self.hatch)
        self.canvas.fig.canvas.draw()
        
    def setColor(self, color):
        self.color = color
        if self.area!=[]:
            for i in range(len(self.area)):
                self.area[i].set_facecolor(self.color)
                self.area[i].set_edgecolor(self.color)
                self.area[i].set_color(self.color)
        self.canvas.fig.canvas.draw()
        
    def setZOrder(self, zorder):
        self.zorder = zorder
        if self.area!=[]:
            for i in range(len(self.area)):
                self.area[i].set_zorder(self.zorder)
        self.canvas.fig.canvas.draw()
        
    def setFill(self, fill):
        self.fill = fill
        if self.area!=[]:
            for i in range(len(self.area)):
                self.area[i].set_fill(self.fill)
        self.canvas.fig.canvas.draw()
        
    def isEmpty(self):
        if self.area==[]:
            return True
        else:
            return False

class displaySpecRegion(object):
    def __init__(self, canvas, waveLimit=None,  visible=False, hatch=None, fill=True, linestyle='-',
                 color='0.7', zorder=3, lw=1.0, alpha=0.5, picker=5):
            self.waveLimit=waveLimit
            self.visible= visible
            self.alpha = alpha
            self.color = color
            self.fill = fill
            self.pic = picker
            self.hatch = hatch
            self.zorder = zorder
            self.canvas = canvas
            self.canvas.pickedSpecRegion = [False, None, None]
            if waveLimit is not None:
                self.area = self.canvas.axes.axvspan(self.waveLimit[0], self.waveLimit[1], color=color,
                                                     linestyle=linestyle, lw=lw, ec=color, fc=color, fill=fill,
                                                     visible=visible, hatch=hatch, zorder=zorder, alpha=alpha,
                                                     picker=picker)
                self.left = self.canvas.axes.axvline(self.waveLimit[0], picker=5.0, color=self.color, gid='left')
                self.right = self.canvas.axes.axvline(self.waveLimit[1], picker=5.0, color=self.color, gid='right')
                self.canvas.fig.canvas.draw()
                if picker:
                    self.cid = self.canvas.fig.canvas.mpl_connect('pick_event', self.onpick)
            else:
                self.area = None
                self.left = None
                self.right = None
    
    def setLimit(self, waveLimit):
        if waveLimit is not None:
            self.waveLimit = waveLimit
            ylim = self.canvas.axes.get_ylim()
            xlim = self.canvas.axes.get_xlim()
            if self.area is None:
                self.area = self.canvas.axes.axvspan(self.waveLimit[0], self.waveLimit[1], color=self.color,
                                                     ec=self.color, fc=self.color,fill=self.fill, visible=self.visible,
                                                     hatch=self.hatch, zorder=self.zorder, alpha=self.alpha)
                self.left = self.canvas.axes.axvline(self.waveLimit[0], color=self.color, picker=self.pic, gid='left')
                self.right = self.canvas.axes.axvline(self.waveLimit[1], color=self.color, picker=self.pic, gid='right')
                self.canvas.axes.set_ylim(ymin=ylim[0], ymax=ylim[1])
                self.canvas.axes.set_xlim(xmin=xlim[0], xmax=xlim[1])
                self.canvas.fig.canvas.draw()
                if self.pic:
                        self.cid = self.canvas.fig.canvas.mpl_connect('pick_event', self.onpick)
            else:
                vertex = [[self.waveLimit[0], 0.0], [self.waveLimit[0], 1.0], [self.waveLimit[1], 1.0],
                          [self.waveLimit[1], 0.0], [self.waveLimit[0], 0.0]]
                self.area.set_xy(vertex)
                self.left.set_data([self.waveLimit[0], self.waveLimit[0]], [0, 1])
                self.right.set_data([self.waveLimit[1], self.waveLimit[1]], [0, 1])
                self.canvas.axes.set_ylim(ymin=ylim[0], ymax=ylim[1])
                self.canvas.axes.set_xlim(xmin=xlim[0], xmax=xlim[1])
                self.canvas.fig.canvas.draw()
                if self.pic:
                        self.cid = self.canvas.fig.canvas.mpl_connect('pick_event', self.onpick)
        else:
            self.emptyRegion()
                    
    def isEmpty(self):
        if self.waveLimit is None or self.waveLimit[1]==self.waveLimit[0]:
            return True
        else:
            return False
    
    def Limit(self):
        return self.waveLimit
        
    def getMask(self, wave, random=0):
        if not self.isEmpty():
            if random==0:
                mask = numpy.logical_and(wave>=self.waveLimit[0], wave<=self.waveLimit[1])
            else:
                low_limit = numpy.random.uniform(self.waveLimit[0] - random / 2.0, self.waveLimit[0] + random / 2.0)
                high_limit = numpy.random.uniform(self.waveLimit[1] - random / 2.0, self.waveLimit[1] + random / 2.0)
                while high_limit<low_limit:
                    high_limit = numpy.random.uniform(self.waveLimit[1] - random / 2.0, self.waveLimit[1] + random / 2.0)
                mask = numpy.logical_and(wave>=low_limit, wave<=high_limit)
            return mask
        else:
            raise UnfilledMaskError
     
    def copyMask(self, mask):
        if not mask.isEmpty():
            self.setLimit(mask.Limit()) 
        else:
            self.emptyRegion()

    def setVisible(self, visible):
            self.visible = visible
            if self.waveLimit is not None:
                self.area.set_visible(self.visible)
                self.left.set_visible(self.visible)
                self.right.set_visible(self.visible)
            self.canvas.fig.canvas.draw()
    
    def setLineStyle(self, linestyle):
        if self.right is not None and self.left is not None:
            self.right.set_linestyle(linestyle)
            self.left.set_linestyle(linestyle)
        self.canvas.fig.canvas.draw()
        
    def setLineWidth(self, linewidth):
        if self.right is not None and self.left is not None:
            self.right.set_lw(linewidth)
            self.left.set_lw(linewidth)
        self.canvas.fig.canvas.draw()

    def setAlpha(self, alpha):
        self.alpha = alpha
        if self.waveLimit is not None:
            self.area.set_alpha(self.alpha)
            self.right.set_alpha(self.alpha)
            self.left.set_alpha(self.alpha)
        self.canvas.fig.canvas.draw()
        
    def setHatch(self, hatch):
        self.hatch = hatch
        if self.waveLimit is not None:
            self.area.set_hatch(self.hatch)
        self.canvas.fig.canvas.draw()
        
    def setColor(self, color):
        self.color = color
        if self.waveLimit is not None:
            self.area.set_facecolor(self.color)
            self.area.set_edgecolor(self.color)
            self.area.set_color(self.color)
            self.left.set_color(self.color)
            self.right.set_color(self.color)
        self.canvas.fig.canvas.draw()
        
    def setZOrder(self, zorder):
        self.zorder = zorder
        if self.waveLimit is not None:
            self.area.set_zorder(self.zorder)
            self.left.set_zorder(self.zorder)
            self.right.set_zorder(self.zorder)
        self.canvas.fig.canvas.draw()
        
    def setFill(self, fill):
        self.fill = fill
        if self.waveLimit is not None:
            self.area.set_fill(self.fill)
        self.canvas.fig.canvas.draw()
        
    def setPicker(self, picker):
        self.picker = picker
        if self.waveLimit is not None:
            self.left.set_picker(self.picker)
            self.right.set_picker(self.picker)
        if picker:
            self.cid = self.canvas.fig.canvas.mpl_connect('pick_event', self.onpick)
        else:
            self.canvas.fig.canvas.mpl_disconnect(self.cid)
            
    def emptyRegion(self):
        xlim = self.canvas.axes.get_xlim()
        ylim = self.canvas.axes.get_ylim()
        if self.waveLimit is not None:
            self.waveLimit  = None
            self.area.remove()
            self.area = None
            self.left.remove()
            self.left = None
            self.right.remove()
            self.right = None
            self.canvas.axes.set_xlim(xmin=xlim[0], xmax=xlim[1])
            self.canvas.axes.set_ylim(ymin=ylim[0], ymax=ylim[1])
            self.canvas.fig.canvas.draw()
            
    def onpick(self, event):
        thisline = event.artist
        self.canvas.pickedSpecRegion = [True, self, thisline.get_gid()]
        
def masksFilled(masks_list):
    filled = True
    for i in range(len(masks_list)):
        if masks_list[i].isEmpty():
            filled = False
            break
    return filled
