
print('----------------------------------------------------------------')
print('                        Post-processing Obs Dart                ')
print('----------------------------------------------------------------')

#%% Toolboxes

from param_dart import *
from scipy.interpolate import interp1d


for dday in datevec_assim:
  file_prior = dir_obs_diag+'Prior_Diag_'+dday.strftime('%Y%m%d')+'.nc'
  nc_prior = ncdf.Dataset(file_prior,'r')
  T_spread  = np.array(nc_prior.variables['temp'])[0,1,:,:,:]
  S_spread  = np.array(nc_prior.variables['salt'])[0,1,:,:,:]
  U_spread  = np.array(nc_prior.variables['u'])[0,1,:,:,:]
  V_spread  = np.array(nc_prior.variables['v'])[0,1,:,:,:]
  nc_prior.close()

  [nlevs,nlat,nlon] = T_spread.shape

  for i_lon in xrange(nlat):
    for i_lat in xrange(nlon):
       










