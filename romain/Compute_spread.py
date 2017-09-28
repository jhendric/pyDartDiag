# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 14:28:48 2016

@author: romain
"""

print('----------------------------------------------------------------')
print('                        Compute Spread                          ')
print('----------------------------------------------------------------')

import numpy as np
import netCDF4 as ncdf
import datetime as dtime
import rt_dart_tools
import sys
from shutil import copyfile

#%% Parameters

geo = [-98, -45, 10, 52];
simu= 'NWA-RE.REANA04';

# Period
start_date  = dtime.datetime(2011,1,1);
final_date = dtime.datetime(2011,1,31);
N_days = (final_date-start_date).days+1;

# Directories
dir_outputs = '/t0/scratch/romain/dart/tmpdir_'+simu+'/Outputs/'
#dir_outputs = '/Users/romain/Work/Projects/Dart/Data/'+simu+'/Test_rst/'

N_members=30

variables = ['temp','salt','u','v'];

#%% Compute ensemble mean and spread

for i_date in range(9):
    mydate = start_date + dtime.timedelta(i_date)
    print(mydate.strftime('%Y%m%d'))
    filename = dir_outputs + 'Prior/m001/NWA-RE.REANA04_rst_' + mydate.strftime('%Y%m%d') + '.nc'
    nc_file = ncdf.Dataset(filename,'r')
    N=nc_file.dimensions['s_rho'].size
    Nlon=nc_file.dimensions['xi_rho'].size
    Nlat=nc_file.dimensions['eta_rho'].size
    nc_file.close()
    
    # Open a new NetCDF file to write the data to.
    file_diag = dir_outputs+'Diags/Prior_Diag_'+mydate.strftime('%Y%m%d')+'.nc'
    copyfile(dir_outputs+'Diags/Prior_Diag_20110110.nc', file_diag)
    w_nc_fid = ncdf.Dataset(file_diag,'r+')
    
    for i_var,var in enumerate(variables):
        print(var),
        if (var=='u'):
            dims=[N,Nlat,Nlon-1]
        elif (var=='v'):
            dims=[N,Nlat-1,Nlon]
        else:
            dims=[N,Nlat,Nlon]
     
        temp   = np.zeros([N_members]+dims)
        values = np.zeros([1,2]+dims)
        for i_member in range(N_members):
            print i_member,
            sys.stdout.flush()
            filename = dir_outputs + 'Prior/m' + str(i_member+1).zfill(3) + '/NWA-RE.REANA04_rst_' + mydate.strftime('%Y%m%d') + '.nc'
            nc_file = ncdf.Dataset(filename,'r')
            temp[i_member,:,:,:] = nc_file.variables[var][:]
            nc_file.close()
        print ' ' 
        model_state = np.reshape(temp,[N_members,reduce(lambda x, y: x*y, dims)]).T
    
        model_spread = rt_dart_tools.dart_spread(model_state)
        values[0,1,:,:,:] = np.reshape(model_spread,dims)
        values[0,0,:,:,:] = np.mean(temp,0);
        w_nc_fid.variables[var][:,:,:,:,:] = values
    
    
    var='zeta'
    print(var)
    temp   = np.zeros([N_members,Nlat,Nlon])
    values = np.zeros([1,2,Nlat,Nlon])
    for i_member in range(N_members):
        print i_member,
        sys.stdout.flush()
        filename = dir_outputs + 'm' + str(i_member+1).zfill(3) + '/NWA-RE.REANA04_rst_' + mydate.strftime('%Y%m%d') + '.nc'
        nc_file = ncdf.Dataset(filename,'r')
        temp[i_member,:,:] = nc_file.variables[var][:]
    
    model_state = np.reshape(temp,[N_members,Nlat*Nlon]).T
    model_spread = rt_dart_tools.dart_spread(model_state)
    values[0,1,:,:] = np.reshape(model_spread,[Nlat,Nlon])
    values[0,0,:,:] = np.mean(temp,0);
    w_nc_fid.variables[var][:,:,:,:] = values
    
    w_nc_fid.variables['time'][:] = (mydate-dtime.datetime(1601,1,1)).days-1
    
    w_nc_fid.close()  # close the new file



