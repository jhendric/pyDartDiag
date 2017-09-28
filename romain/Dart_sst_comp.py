
print('----------------------------------------------------------------')
print('                        Evolution of SST                        ')
print('----------------------------------------------------------------')

#%% Toolboxes

from param_dart import *

#%% 

lon_pri = RomsGrid.grid.variables['lon_rho'].value-360
lat_pri = RomsGrid.grid.variables['lat_rho'].value

# Mean SST evolution (for colorbar)
avg_file = dir_diag+'Avg_Prior_Diag_timeseries.nc4'
nc_avg = ncdf.Dataset(avg_file,'r')
SST_avg = nc_avg.variables['temp'][:,0,-1]
time_avg_tmp = nc_avg.variables['time'][:]
nc_avg.close()

time_avg = [dtime.datetime(1600,1,1)+dtime.timedelta(dt) for dt in time_avg_tmp]
SST_avg_smooth = rt_stats_tools.loess(SST_avg,1./20)


for dday in datevec_assim:
   figname=dir_pictures + '/SST_comp_avg001_' + dday.strftime('%Y%m%d') + '_' + simu 
   if not os.path.isfile(figname+'.jpg'):

      pri_file = dir_diag+'Prior_Diag_'+(dday-dtime.timedelta(1)).strftime('%Y%m%d')+'.nc4';
      avg_m001 = glob.glob(dir_average +'m001/'+simu+'_avg_'+(dday-dtime.timedelta(1)).strftime('%Y%m%d')+'_*.nc')[0];
      obs_file = glob.glob(dir_obs+'obs_seq.*.final.'+dday.strftime('%Y%m%d')+'.nc')[0];
   
      nc_obs = ncdf.Dataset(obs_file,'r')
      SST_obs = nc_obs.variables['observations'][:,0]
      SST_obs_pri = nc_obs.variables['observations'][:,1]
      lon_obs = nc_obs.variables['location'][:,0]
      lat_obs = nc_obs.variables['location'][:,1]
      obs_type  = nc_obs.variables['obs_type'][:]
      nc_obs.close()
      idx_SST = (obs_type==52)
      SST_obs = SST_obs[idx_SST]
      SST_obs_pri = SST_obs_pri[idx_SST]
      lon_obs = lon_obs[idx_SST]
      lat_obs = lat_obs[idx_SST]
      
      nc_pri = ncdf.Dataset(pri_file,'r')
      SST_pri = np.squeeze(nc_pri.variables['temp'][:,0,-1,:,:])
      nc_pri.close()

#      nc_pri = ncdf.Dataset(avg_m001,'r')
#      SST_pri = np.squeeze(nc_pri.variables['temp'][:,-1,:,:])
#      nc_pri.close()

      clip = SST_avg_smooth[(time_avg==dday)+0] +[-12,12]
      fig = plt.figure(figsize=[20.,10.])
      plt.clf()
      # Plot observations
      m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),subpltid=121,fontsiz=14,plotitle='Observations')
      p=m.scatter(lon_obs, lat_obs, c=SST_obs,edgecolors='none',s=10,cmap=rt_colormaps['intense2'],vmin=clip[0],vmax=clip[1])
      cb=m.colorbar(pad="8%")
      #clip=p.get_clim()
      # Plot ensemble mean
      m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),subpltid=122,fontsiz=14,plotitle='Model estimate')
      m.pcolor(lon_pri,lat_pri,SST_pri,cmap=rt_colormaps['intense2'],vmin=clip[0],vmax=clip[1])
      cb=m.colorbar(pad="8%")
      
      plt.savefig(figname+'.png')
      plt.close(fig)
      os.system('convert '+figname+'.png'+' '+figname+'.jpg')
      os.system('rm '+figname+'.png')

      print(figname+'.jpg')




