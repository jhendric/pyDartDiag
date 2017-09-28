# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 14:35:27 2016

@author: romain
"""

print('----------------------------------------------------------------')
print('                        Post-processing Obs Dart                ')
print('----------------------------------------------------------------')

#%% Toolboxes

from param_dart import *

#%% Diagnosis

file_obs_diag = dir_obs_diag+'obs_diag_romain.nc'
nc_diags = ncdf.Dataset(file_obs_diag,'r')
date_vec = [dtime.datetime(1900,1,1)+dtime.timedelta(dt) for dt in nc_diags.variables['time'][:]]
fds = mpl_dates.date2num(date_vec) # converted

variname = nc_diags.Variable_type.split(',')[0:-1]
copyname = nc_diags.Copy.split(',')[0:-1]
diagname = [u'RMSE',u'Bias',u'Spread',u'TotalSpread']
n_diag = len(diagname)
n_copy = len(copyname)
n_var  = len(variname)
n_lat  = len(nc_diags.dimensions['lat_cell'])
n_lon  = len(nc_diags.dimensions['lon_cell'])

lon_cell = nc_diags.variables['lon_cell'][:]
lat_cell = nc_diags.variables['lat_cell'][:]
lon_map,lat_map = np.meshgrid(lon_cell,lat_cell)
diag_map = np.ma.empty((n_diag,n_copy,n_var,n_lat,n_lon))

for i_diag in xrange(0,n_diag):
   diag_map[i_diag,:,:,:,:] = nc_diags.variables[diagname[i_diag]+'_map'][:]

rmse_map = nc_diags.variables['RMSE_map'][:]
bias_map = nc_diags.variables['Bias_map'][:]
spre_map = nc_diags.variables['Spread_map'][:]
totspre_map = nc_diags.variables['TotalSpread_map'][:]

nc_diags.close()

clim = [[0 3],[-2 2],[0 1],[0 3]]
pal  = [rt_colormaps['eke2'],rt_colormaps['redblueclass'],rt_colormaps['eke2'],rt_colormaps['eke2']]

for i_var in xrange(0,n_var):
   fig = plt.figure(figsize=[25.,13.]);plt.clf()
   for i_diag in xrange(0,n_diag):
      for i_copy in xrange(0,n_copy):
         # Create a subplot for each diag
         # Plot pcolor
         subpltid=n_copy*100+n_diag*10+(i_copy*n_diag+1+i_diag)
         m=rt_plotbox.rt_plot_2D(lon_map,lat_map,diag_map[i_diag,i_copy,i_var,:,:],
                                 subpltid=subpltid,fontsiz=14,plotitle=diagname[i_diag]+' '+copyname[i_copy],
                                 clim=clim[i_diag],cstep=100,pal=pal[i_diag])
       
   figname=dir_pictures + '/Diags_rt_map_all_' + simu + '_' + variname[i_var] + '.png'
   plt.savefig(figname)
   print(figname)

plt.close('all')


