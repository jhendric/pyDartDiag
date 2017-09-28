

#%% Toolboxes

from param_dart import *

#%% Load data

dir_data = '/Users/romain/Work/Projects/Dart/Data/Init/'
prefix = 'HYCOM_GLBa0.08_2011_001_ClimCore2_NWA_y'

N_members = 30
N_lat = 362
N_lon = 722

file_grd = '/Users/romain/Work/Projects/Dart/Data/NWA_grd_newwtypechl.nc'
nc_grd = ncdf.Dataset(file_grd,'r')
lon = nc_grd.variables['lon_rho'][:]-360
lat = nc_grd.variables['lat_rho'][:]
nc_grd.close()

N_lat,N_lon = lon.shape

SST = np.ma.empty((N_members,N_lat,N_lon))

for i_member in xrange(N_members):
   file_ini = dir_data+prefix+str(i_member+1).zfill(4)+'.nc'
   nc_ini = ncdf.Dataset(file_ini,'r')
   SST[i_member,:,:] = nc_ini.variables['temp'][:,-1,:,:]
   nc_ini.close()

SST_spread = rt_dart_tools.dart_spread(SST.reshape(-1,30))
SST_spread = SST_spread.reshape(N_lat,N_lon)


figname=dir_data + 'Spread_SST_init.png'
fig = plt.figure(figsize=[20.,15.])
plt.clf()
m=rt_plotbox.rt_plot_2D(lon,lat,SST_spread,fontsiz=14,plotitle='Spread',colorbar=False)
cb=m.colorbar(pad="8%")
plt.savefig(figname)
print(figname)



