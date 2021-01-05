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



import numpy, math
try:
    import pyfits
except:
    from astropy.io import fits as pyfits
from scipy import ndimage
from own_exceptions import *

__version__ = '0.1.2'

class IFUcube(object):
    """This is the main IFU datacube class"""
    
    def __init__(self,dataCube=[],errCube=[],wave=[],xScale=0,yScale=0):
        if dataCube == []:
            self.dataCube = []
            self.errCube = []
            self.wave = []
            self.crval3 = []
            self.cdelt3 = []
            self.naxis3 = []
            self.wDim = 0
            self.xDim = 0
            self.yDim = 0
            self.xScale = 0
            self.yScale = 0
            self.header = []
            self.empty = True
        else:
            self.dataCube = dataCube
            self.errCube = errCube
            self.wave = wave
            self.crval3 = [wave[0]]
            self.cdelt3 = [wave[1]-wave[0]]
            self.naxis3 = [wave.shape[0]]
            self.wDim = wave.shape[0]
            self.xDim = dataCube.shape[2]
            self.yDim = dataCube.shape[1]
            self.xScale = xScale
            self.yScale = yScale
            self.header = []
            self.empty = False

    def loadFitsCube(self,name_dat,name_err=None,name_var=None,xscale=1,yscale=1,hdu=0):
            ### Open Fits file
            fits = pyfits.open(name_dat)
            if hdu==0:
                if fits[hdu].data is None:
                    hdu=1
            dat = fits[hdu].data
            dim = dat.shape

            ### Testing whether the data has 3 dimensions, if not raise error
            if len(dim)==3:

                ###  Fill all instance variables
                self.dataCube = dat
                self.header = fits[hdu].header
                self.wDim = dim[0]
                self.yDim = dim[1]
                self.xDim = dim[2]
                self.xScale = xscale
                self.yScale = yscale
                self.crval3 = [self.header['crval3']]
                self.cdelt3 = [self.header['cdelt3']]
                self.naxis3 = [self.header['naxis3']]

                ### Create the wavelength array 
                wave = numpy.zeros(self.wDim,dtype="float32")
                for i in range(len(self.naxis3)):
                    if i == 0:
                        wave[0:self.naxis3[i]] = numpy.arange(self.naxis3[i])*self.cdelt3[i]+self.crval3[i]
                    elif i>0:
                        wave[self.naxis3[i-1]:self.naxis3[i]] = numpy.arange(self.naxis3[i])*self.cdelt3[i]+self.crval3[i]
                self.wave = wave
                self.empty = False

                ### Reading corresponding variance frame when given
                if not name_err==None:
                    fits = pyfits.open(name_err)
                    err = fits[hdu].data
                    dim_err = err.shape
                    ### Test whether the cube has 3 Dimensions
                    if len(dim)==3:
                        self.errCube=err
                    else:
                        raise IFUcubeIOError("The Frame is not an IFU cube!")

                ### Reading corresponding variance frame when given
                if not name_var==None:
                    fits = pyfits.open(name_var)
                    var = fits[hdu].data
                    dim_var = var.shape
                    ### Test whether the cube has 3 Dimensions
                    if len(dim)==3:
                        self.errCube=numpy.sqrt(var)
                    else:
                        raise IFUcubeIOError("The Frame is not an IFU cube")
            else:
                raise IFUcubeIOError("The Frame is not an IFU cube" )
                
                
    def loadFitsVarCube(self,name_var,hdu=0):
        fits = pyfits.open(name_var)
        dat = numpy.sqrt(fits[hdu].data)
        hdr = fits[0].header
        dim = dat.shape
        if dim!=(self.wDim, self.yDim, self.xDim) or [hdr['crval3']]!=self.crval3 or [hdr['cdelt3']]!=self.cdelt3:
            raise IFUcubeIOError("This is not a corresponding IFU Variance cube")
        else:
            self.errCube = dat
            
    def errorRandomCube(self):
        new = numpy.random.normal(self.dataCube, self.errCube)
        newCube= IFUcube(numpy.array(new, dtype=numpy.float32), wave=self.wave)
        return newCube
                
                

    def emptyCube(self):
        self.dataCube = []
        self.errCube = []
        self.wave = []
        self.crval3 = []
        self.cdelt3 = []
        self.naxis3 = []
        self.wDim = 0
        self.xDim = 0
        self.yDim = 0
        self.xScale = 0
        self.yScale = 0
        self.header = []
        self.empty = True
        
    def subCube(self,start_wave,end_wave,region=[]):
        """Changes the wavelength range of the IFU data cube to the range within the given start and end values"""

        ## Select the desired wavelength range
        selectWave = numpy.logical_and(self.wave>=start_wave,self.wave<=end_wave)
        self.wave = self.wave[selectWave]
        self.wDim = numpy.sum(selectWave)
        self.naxis3 = [self.wDim]
        self.crval3 = [self.wave[0]]
        ## Select the required region and update the data structure
        if region:
            self.dataCube = self.dataCube[selectWave,region[2]:region[3],region[0]:region[1]]
        else:
            self.dataCube = self.dataCube[selectWave,:,:]

    def writeFitsData(self,nameDat):
        """Write the current IFU data cube to a FITS file"""

        if self.empty == False:
            hdu = pyfits.PrimaryHDU(self.dataCube)
            
            ## Update header
            if not self.header == []:
                hdu.header = self.header
            hdu.header['crval3']=self.crval3[0]
            hdu.header['cdelt3']=self.cdelt3[0]
            hdu.header['crval2']=0
            hdu.header['cdelt2']=self.yScale
            hdu.header['crval1']=0
            hdu.header['cdelt1']=self.xScale
            hdu.writeto(nameDat,clobber=True)
        else:
           raise IFUcubeIOError("The Frame is not an IFU cube" )

    def writeFitsErr(self,nameErr):

        if self.emtpy == False and len(self.errCube.shape)==3:
            hdu = pyfits.PrimaryHDU(self.errCube)

            ## Update header
            if not self.header == []:
                hdu.header = self.header
            hdu.header.update('crval3',self.crval3[0])
            hdu.header.update('cdelt3',self.cdelt3[0])
            hdu.header.update('crval2',0)
            hdu.header.update('cdelt2',self.yScale)
            hdu.header.update('crval1',0)
            hdu.header.update('cdelt1',self.xScale)
            hdu.writeto(nameErr,clobber=True)
        else:
           raise IFUcubeIOError("The Frame is not an IFU cube" )
    
    def isEmpty(self):
        return self.empty

    def findCenterSimple(self,region=None):
        """Estimate the Object center as a function of Wavelength using a simple center of mass algorithm"""

        centers = numpy.zeros((2,self.wDim),dtype="float32")
        if region == None:
            for i in range(self.wDim):
                centers[:,i] = ndimage.center_of_mass(self.dataCube[i,:,:]) 

        else: 
            for i in range(self.wDim):
                centers[:,i] = ndimage.center_of_mass(self.dataCube[i,region[2]:region[3],region[0]:region[1]])

        return centers,[numpy.median(centers[0,:]),numpy.median(centers[1,:])]

    
    def findMaximum(self):
        """Find the Maximum spaxel as a function of wavelength"""
    
        maximum = numpy.zeros((2,self.wDim),dtype="float32")
        self.dataCube[numpy.isnan(self.dataCube)]=0
        for i in range(self.wDim):
	    maximum_slice = ndimage.measurements.maximum_position(self.dataCube[i,:,:])
            maximum[:,i] = [maximum_slice[0], maximum_slice[1]]
	print [numpy.median(maximum[0,:]),numpy.median(maximum[1,:])]
        return maximum,[numpy.median(maximum[0,:]),numpy.median(maximum[1,:])]
                

    def extractImage(self,start_wave,end_wave,mode='sum'):
        """Extract an image from the IFU cube in the given wavelength range. Available modes are 'sum','median','mean'."""

        if self.empty == False:
            selectWave = numpy.logical_and(self.wave>=start_wave,self.wave<=end_wave)
            if mode == 'sum':
                image = numpy.sum(self.dataCube[selectWave,:,:],0)
            elif mode == 'median':
                image = numpy.median(self.dataCube[selectWave,:,:],0)
            elif mode == 'mean':
                image = numpy.mean(self.dataCube[selectWave,:,:],0)
            return image
        else:
            raise IFUcubeIOError("No data in IFU cube object" )
            
    def extractImageMask(self,mask,mode='sum'):
        """Extract an image from the IFU cube in the given Mask. Available modes are 'sum','median','mean'."""
        
        if mask.shape[0]!=self.wDim:
            raise IFUcubeIOError("Mask does not match wavelength dimension" )
        if self.empty == False:
            if mode == 'sum':
                image = numpy.sum(self.dataCube[mask,:,:],0)
            elif mode == 'median':
                image = numpy.median(self.dataCube[mask,:,:],0)
            elif mode == 'mean':
                image = numpy.mean(self.dataCube[mask,:,:],0)
            return image
        else:
            raise IFUcubeIOError("No data in IFU cube object" )
            
    
    
    def extractSpecMask(self, mask, mode='sum'):
        if self.empty == False and self.xDim == mask.shape[1] and self.yDim == mask.shape[0]:
            rss = numpy.reshape(self.dataCube, (self.wDim, self.yDim*self.xDim), 'C')
            ma_rss = numpy.reshape(mask, (self.yDim*self.xDim), 'c')
            if mode == 'sum':
                spec = numpy.sum(rss[:, ma_rss],1)
            elif mode == 'median':
                spec = numpy.median(rss[:, ma_rss],1)
            elif mode == 'mean':
                spec = numpy.mean(rss[:, ma_rss],1)
            return spec
        elif self.empty == False and (self.xDim != mask.shape[1] or self.yDim != mask.shape[0]):
            raise IFUcubeIOError("Cube Operation on a wrong shape")
        else:
            raise IFUcubeIOError("No data in IFU cube object" )
    
    def deblendQSOHost(self, center,qso_mask, broad_region, cont_region, iter, mode,  eelr_mask=None, interpolate_cont=False, subtract_region=None,  radius=None, factor=None, host_image=None, showProgress=None):
        if showProgress!=None:
            showProgress.setValue(0)
            showProgress.setLabelText('Performing Iteration %i/%i'%(1, iter))
        else:
            abort=False
        
        if radius!=None and radius!=0.0:
            psf_map_cut = self.dataCube[10, :, :]
            psf_map_cut[numpy.logical_not(qso_mask)]==0
            if center!=None:
                center = [center[1][0], center[1][1]]
            else:
                select = psf_map_cut==numpy.max(psf_map_cut)
                idx_row, idx_col = numpy.indices(psf_map_cut.shape)
                center= [idx_row[select][0], idx_col[select][0]]
            radius_mask = numpy.fromfunction(lambda i, j: numpy.sqrt((i-center[0])**2+(j-center[1])**2)<=radius, (self.yDim,  self.xDim), dtype=int)
        else:
            radius_mask = numpy.ones((self.yDim, self.xDim), dtype=int)
        qso_spec_0 = self.extractSpecMask(qso_mask, mode='mean')   
        if factor==None and host_image==None:
            scale_eelr  = 1.0

        elif factor!=None:
            scale_eelr=factor
            
        for i in range(iter):
            if showProgress!=None:
                abort=showProgress.wasCanceled()
                showProgress.setLabelText('Performing Iteration %i/%i'%(i+1, iter))
            if not abort:
                if i == 0:
                    spec = qso_spec_0
                else:
                    if showProgress!=None:
                        showProgress.setValue(i+1)
                    if host_image!=None:
                        cent = ndimage.measurements.maximum_position(scale)
                        dim = host_image.shape
                        psf = scale[cent[0]-3:cent[0]+3+1, cent[1]-3:cent[1]+3+1]
                        
                        host_smoothed=numpy.array(ndimage.filters.convolve(host_image, psf, mode='constant'))
                        qso_region = numpy.sum(host_smoothed[qso_mask].flatten())/(numpy.sum(qso_mask))
                        eelr_region = numpy.sum(host_smoothed[eelr_mask].flatten())/(numpy.sum(eelr_mask))
                        scale_eelr = qso_region/eelr_region
    
                    if eelr_mask!=None:
                        eelr_spec = EELR_cube_temp.extractSpecMask(eelr_mask, mode='mean')
                        spec = qso_spec_0-eelr_spec*scale_eelr
                    else:
                        spec = qso_spec_0
 
                wave_select_cont=numpy.logical_or(cont_region[0], cont_region[1])
                wave_select_broad=numpy.logical_or(broad_region[0], broad_region[1])
	
                
                if interpolate_cont==False:
                    cont_flux_mean = numpy.median(spec[wave_select_cont])
                    qso_spec = spec-cont_flux_mean
                else:
                    wave_select_cont1=cont_region[0]
                    wave_select_cont2=cont_region[1]
                    point_y1 = numpy.median(spec[wave_select_cont1])
                    point_y2 = numpy.median(spec[wave_select_cont2])
                    points_x = [numpy.median(self.wave[wave_select_cont1]),numpy.median(self.wave[wave_select_cont2]),numpy.median(self.wave[wave_select_cont2])]
                    point_x1 = points_x[0]
                    point_x2 = points_x[1]      
    
                    a1 = (point_y1-point_y2)/(point_x1-point_x2)
                    b1 = point_y1-a1*point_x1
                        
                    qso_continuum = b1+a1*self.wave
                    qso_spec = spec-qso_continuum
          
                    
                    
                if mode=='sum':
                    broad_flux_mean = numpy.sum(qso_spec[wave_select_broad])
                elif mode=='median':
                    broad_flux_mean = numpy.median(qso_spec[wave_select_broad])
                elif mode=='mean':
                    broad_flux_mean = numpy.mean(qso_spec[wave_select_broad]) 
        
                if interpolate_cont==False:
                    cont_flux = self.extractImageMask(wave_select_cont, mode='median')
                    broad_flux = self.extractImageMask(wave_select_broad,mode)
            
                    
                    if mode=='median' or mode=='mean':
                        scale = (broad_flux-cont_flux)/(broad_flux_mean)
                    elif mode=='sum':
                        scale = (broad_flux-(cont_flux*numpy.sum(wave_select_broad)))/(broad_flux_mean)
                    
                else:
                    point_y1 = self.extractImageMask(cont_region[0], mode='median')
                    point_y2 = self.extractImageMask(cont_region[1], mode='median')
                    point_x1 = points_x[0]
                    point_x2 = points_x[1]
                
                    a1 = (point_y1-point_y2)/(point_x1-point_x2)
                    b1 = point_y1-a1*point_x1
                
                    lin_cube = self.wave[:, numpy.newaxis, numpy.newaxis]*a1[numpy.newaxis, :,:]+b1[numpy.newaxis, :,:]
                    cont_free = self.dataCube-lin_cube
                    if mode=='sum':
                        broad_flux = numpy.sum(cont_free[wave_select_broad, :, :], 0)
                    elif mode=='median':
                        broad_flux = numpy.median(cont_free[wave_select_broad, :, :], 0)
                    elif mode=='mean':
                        broad_flux = numpy.mean(cont_free[wave_select_broad, :, :], 0)
                
                    scale=broad_flux/(broad_flux_mean)
     #           if i==1:
      #              print spec-qso_continuum
                    
                   
                dataQSO_cube =  spec[:, numpy.newaxis, numpy.newaxis] * scale[numpy.newaxis, :,:]*radius_mask
                if  subtract_region!=None:
                    mask = numpy.logical_not(subtract_region)
                    dataQSO_cube[:, mask] = 0.0
                
                
                EELR_cube_temp= IFUcube(self.dataCube - dataQSO_cube, wave=self.wave)
        if not abort:    
            EELR_cube = EELR_cube_temp
            QSO_cube = IFUcube(dataCube=dataQSO_cube, wave=self.wave)
        else:
            EELR_cube = None
            QSO_cube = None
        
        return EELR_cube, QSO_cube
       
       
def max_img(img):
    select = img==numpy.max(img)
    idx_row, idx_col = numpy.indices(img.shape)
    return idx_row[select], idx_col[select]
    
