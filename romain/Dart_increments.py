# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 14:32:51 2016

@author: romain
"""

print('----------------------------------------------------------------')
print('                        Post-processing Obs Dart                ')
print('----------------------------------------------------------------')

#%% Toolboxes

from param_dart import *


#%% P/P Diags files

prio_diag_file = dir_obs_diag+'Prior_Diag_'    +start_assim.strftime('%Y%m%d')+'.nc';
post_diag_file = dir_obs_diag+'Posterior_Diag_'+start_assim.strftime('%Y%m%d')+'.nc';

nc_prio = ncdf.Dataset(prio_diag_file,'r')
lon=np.array(nc_prio.variables['lon_rho'])-360
lat=np.array(nc_prio.variables['lat_rho'])
mask=np.array(nc_prio.variables['mask_rho'])

fig = plt.figure(figsize=[10.,7.])
plt.clf()

for i_date in range(N_days):
    mydate=start_assim+dtime.timedelta(i_date)
    prio_diag_file = dir_obs_diag+'Prior_Diag_'    +mydate.strftime('%Y%m%d')+'.nc';
    post_diag_file = dir_obs_diag+'Posterior_Diag_'+mydate.strftime('%Y%m%d')+'.nc';
    
    nc_prio = ncdf.Dataset(prio_diag_file,'r')
    nc_post = ncdf.Dataset(post_diag_file,'r')

    prio_temp = nc_prio.variables['temp'][0,0,39,:,:]
    post_temp = nc_post.variables['temp'][0,0,39,:,:]
    
    m=rt_plotbox.rt_plot_2D(lon,lat,post_temp-prio_temp,
                            pal=rt_colormaps['redblueclass'],clim=[-5,5],fontsiz=18,
                            plotitle='Increment for ' + mydate.strftime('%Y-%m-%d'),colorbar=False)
    cb=m.colorbar(pad="8%")
    cb.ax.tick_params(labelsize=18) 

    figname=dir_pictures + '/Increment_' + simu + '_' + mydate.strftime('%Y%m%d') + '.png'
    plt.savefig(figname)
    print(figname)
    

