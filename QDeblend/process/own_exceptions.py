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

__version__='0.1.2'

class UnfilledMaskError(Exception):
    def __init__(self):
        self.msg="A required mask was not properly definied!"
        
class EmptyHostImage(Exception):
    def __init__(self):
        self.msg="The host image was not definied!"

class IFUcubeIOError(Exception):
    def __init__(self, msg):
        self.msg=msg
