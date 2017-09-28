# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 11:08:37 2016

@author: romain
"""

import numpy as np
import rt_netcdf_tools
import collections
import datetime as dtime

class romsGrid:

   def __init__(self,gridname):
      self.filename = gridname

   def get_grid(self):
      self.grid = rt_netcdf_tools.get_nc_object(self.filename)

   def get_std_depths(self,vtransform=2,vstretching=4):
      nlat = self.grid.dimensions['eta_rho']
      nlon = self.grid.dimensions['xi_rho']
      zeta=np.zeros((nlat,nlon))
      z_r = get_depths(self.grid,zeta,'r',vtransform,vstretching)
      z_w = get_depths(self.grid,zeta,'w',vtransform,vstretching)
      z_r_att=collections.OrderedDict([\
         ('long_name','standard depth of sigma levels at RHO-points'),\
         ('units','meters')])
      z_w_att=collections.OrderedDict([\
         ('long_name','standard depth of sigma levels at W-points'),\
         ('units','meters')])
      self.grid.add_variable('z_r',z_r,vardim=('s_rho','eta_rho','xi_rho'),varatt=z_r_att)
      self.grid.add_variable('z_w',z_w,vardim=('s_w','eta_rho','xi_rho'),varatt=z_w_att)

   def write_grid(self,filename):
      self.grid.create_file(filename)

   def __repr__(self):
      return 'ROMS grid (from \''+self.filename+'\')'


def get_depths(grid,zeta,vtype,vtransform,vstretching):

   # Get values from grid
   h = grid.variables['h'].value
   theta_s = float(grid.variables['theta_s'].value)
   theta_b = float(grid.variables['theta_b'].value)
   hc = float(grid.variables['hc'].value)
   N = grid.dimensions['s_rho']
   [nlat,nlon] = h.shape

   # Fractional vertical stretching coordinate
   if (vtype == 'w'):
      N = N+1
      sc = np.linspace(-1,0,num=N)
   else:
      sc = np.linspace(-1,0,num=N,endpoint=False)+1./80

   # Compute vertical stretching functions
   Cs = _Cstretch(vstretching,theta_s,theta_b,sc)

   # Nonlinear vertical transformation
   z = np.empty((N,nlat,nlon))
   if (vtransform==1):
      for i_lev in xrange(N):
         S = hc*sc[i_lev]+(h-hc)*Cs[i_lev]
         z[i_lev,:,:] = S + zeta * \
                       (1.0 + S/h)
   else:
      for i_lev in xrange(N):
         S = (hc*sc[i_lev]+h*Cs[i_lev]) / \
             (hc + h)
         z[i_lev,:,:] = zeta + [zeta + h] * S

   return z   


def _Cstretch(vstretching,theta_s,theta_b,sc):
   # Routine to compute Cs

   if (vstretching==1):
      cff1 = 1./np.sinh(theta_s)
      cff2 = 0.5/np.tanh(0.5*theta_s)
      Cs=(1.-theta_b)*cff1*sinh(theta_s*sc)+ \
        theta_b*(cff2*tanh(theta_s*(sc+0.5))-0.5)

   elif (vstretching==2):
      Aweight = 1
      Bweight = 1
      if (theta_s > 0):
         Csur = (1.0 - np.cosh(theta_s * sc)) / \
                      (np.cosh(theta_s) - 1.0)
         if (theta_b > 0):
            Cbot = np.sinh(theta_b * (sc + 1.0)) / \
               np.sinh(theta_b) - 1.0
            Cweight = (s_rho + 1.0)**Aweight * \
                   (1.0 + (Aweight / Bweight) * \
                   (1.0 - (s_rho + 1.0)**Bweight))
            Cs_r = Cweight * Csur + (1.0 - Cweight) * Cbot
         else:
            Cs = Csur
      else:
         Cs = sc

   elif (vstretching==4):
      if (theta_s > 0):
         Csur = (1.0 - np.cosh(theta_s * sc)) / \
                     (np.cosh(theta_s) - 1.0)
      else:
         Csur = -sc**2
      if (theta_b > 0):
         Cbot = (np.exp(theta_b * Csur) - 1.0) / \
              (1.0 - np.exp(-theta_b) )
         Cs = Cbot
      else:
         Cs = Csur

   return Cs










