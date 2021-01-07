#!/usr/bin/env python
import setuptools

setuptools(name='QDeblend3D',
      version='1.4.0b',
      description="""Graphical User Interface for visualzing astronomical optical/NIR IFU datacubes and subtracting 
                  point-like unobscured AGN contributions from the data. 
                  """,
      author='Bernd Husemann',
      author_email='berndhusemann@gmx.de',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2 :: Only',
            'Topic :: Scientific/Engineering :: Astronomy'.
            'Topic :: Scientific/Engineering :: Image Processing'
      ]
      packages=setuptools.find_packages(),
      url='http://github.com/brandherd/QDeblend3D',
      install_requires=['astropy==1.3.3','numpy==1.11.3','astropy==1.3.3','matplotlib==1.5.3','pyqt==4.11.4'],
      python_requires='>=2.7, <3.0',
      scripts=['bin/QDeblend'])
