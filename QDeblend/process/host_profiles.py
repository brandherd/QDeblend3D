import numpy, math
from scipy import special

"""
The Sersic Profile
Formulae for Sersic profile taken from Graham & Driver (2005)
bibcode: 2005PASA...22..118G
"""
class Sersic:
    def __init__(self, size, x_c, y_c, mag, n, r_e, e=0., theta=0., osfactor=10,
                 osradius=2):

        self.size  = size
        self.x_c   = x_c
        self.y_c   = y_c
        self.n     = n
        self.r_e   = r_e
        self.e     = e
        self.theta = theta
        self.osf   = osfactor
        self.osr   = osradius


        flux = 10**(-0.4*mag)

        self._get_kappa()
        self.sigma_e = flux/(2*math.pi*(r_e**2)*math.exp(self.kappa)*n*
                             (self.kappa)**(-2.*n)*special.gamma(2.*n)*(1.-e))

        self._make_array()

    def _get_kappa(self):
        init = 1.9992*self.n - 0.3271
        self.kappa = self.__newton_it(init)

    def __newton_it(self, x0, epsilon=1e-8):
        for i in range(2000):
            x0 -= self.__gammainc(x0)[0]/self.__gammainc(x0)[1]
            if abs(self.__gammainc(x0)[0]) <= epsilon:
                break
            if i == 1999:
                print 'Warning: Iteration failed!'
        return x0

                    
    def __gammainc(self, x):
        f  = special.gammainc(2*self.n, x) - 0.5
        df = (math.exp(-x) * x**(2.*self.n - 1.))/special.gamma(2.*self.n)
        return (f, df)


    def _make_array(self):
        self.array = numpy.fromfunction(self._draw, self.size, dtype='float32')
        if self.osf != 1:
            csize = ((2*self.osr+1)*self.osf, (2*self.osr+1)*self.osf)
            x_n = int(round(self.x_c))
            y_n = int(round(self.y_c))

            self.x_c += (self.osr - round(self.x_c))
            self.y_c += (self.osr - round(self.y_c))
            self.x_c *= self.osf
            self.y_c *= self.osf
            self.x_c += 0.5*(self.osf-1.)
            self.y_c += 0.5*(self.osf-1.)

            self.r_e *= self.osf
            self.sigma_e /= (self.osf)**2

            carray = numpy.fromfunction(self._draw, csize, dtype='float32')
            
            s1_size = (2*self.osr+1, (2*self.osr+1)*self.osf, self.osf)
            s2_size = (2*self.osr+1, 2*self.osr+1, self.osf)
            step1 = numpy.sum(numpy.reshape(carray, s1_size, 'C'), axis=2)
            step2 = numpy.sum(numpy.reshape(step1, s2_size, 'F'), axis=2)
        
            self.array[y_n-self.osr:y_n+self.osr+1,
                       x_n-self.osr:x_n+self.osr+1] = step2

    def _draw(self, y, x):
        u = (x-self.x_c)*math.sin(self.theta)-(y-self.y_c)*math.cos(self.theta)
        v = (y-self.y_c)*math.sin(self.theta)+(x-self.x_c)*math.cos(self.theta)
        r = numpy.sqrt(u**2 + (v/(1. - self.e))**2)
        return self.sigma_e*numpy.exp(-self.kappa*((r/self.r_e)**(1/self.n)-1))

def cut_area(in_array, center, radius, output=''):
    x_i = round(center[0], 0)
    y_i = round(center[1], 0)

    shape = in_array.shape
    out_array = numpy.zeros((2*radius+1, 2*radius+1), dtype='float32')
    out_shape = out_array.shape

    xmin = max(0, int(x_i - radius))
    xmax = min(shape[1], int(x_i + radius + 1))
    ymin = max(0, int(y_i - radius))
    ymax = min(shape[0], int(y_i + radius + 1))

    xlo = max(0, int(radius - x_i))
    xhi = out_shape[1] - max(0, int(x_i + radius + 1 - shape[1]))
    ylo = max(0, int(radius - y_i))
    yhi = out_shape[0] - max(0, int(y_i + radius + 1 - shape[0]))

    out_array[ylo:yhi,xlo:xhi] = in_array[ymin:ymax,xmin:xmax]

    if output == 'full':
        filled_pix = numpy.zeros(out_shape, dtype='int16')
        filled_pix[ylo:yhi,xlo:xhi] += 1
        return out_array, filled_pix
    else:
        return out_array

def paste_area(in_array, out_shape, refpix_in, refpix_out, out_array=None):
    xpix_in = int(round(refpix_in[0], 0))
    ypix_in = int(round(refpix_in[1], 0))

    xpix_out = int(round(refpix_out[0], 0))
    ypix_out = int(round(refpix_out[1], 0))

    in_shape = in_array.shape
    xmin = max(0, xpix_in - xpix_out)
    xmax = in_shape[1] - max(0, (in_shape[1]-xpix_in) - (out_shape[1]-xpix_out))
    ymin = max(0, ypix_in - ypix_out)
    ymax = in_shape[0] - max(0, (in_shape[0]-ypix_in) - (out_shape[0]-ypix_out))

    xlo = max(0, xpix_out - xpix_in)
    xhi = out_shape[1] - max(0, (out_shape[1]-xpix_out) - (in_shape[1]-xpix_in))
    ylo = max(0, ypix_out - ypix_in)
    yhi = out_shape[0] - max(0, (out_shape[0]-ypix_out) - (in_shape[0]-ypix_in))

    if out_array is None:
        out_array = numpy.zeros(out_shape, dtype='float32')
    
    if ylo < out_array.shape[0] and yhi > 0:
        if xlo < out_array.shape[1] and xhi > 0:
            out_array[ylo:yhi, xlo:xhi] = in_array[ymin:ymax, xmin:xmax]
    return out_array