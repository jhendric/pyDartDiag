
print('----------------------------------------------------------------')
print('                        Post-processing Obs Dart                ')
print('----------------------------------------------------------------')

#%% Toolboxes

from param_dart import *
import rt_netcdf_tools
import rt_stats_tools
import collections
import sys

lon_rho = RomsGrid.grid.variables['lon_rho'].value-360
lat_rho = RomsGrid.grid.variables['lat_rho'].value

#########################################################################################
#%% Parameters
#########################################################################################
dir_hindc = ['/Volumes/P10/ROMS/NWA/','/Volumes/P10/ROMS/NWA/','/Volumes/P8/ROMS/NWA/']
simus_hindc = ['NWA-RD.HCSODA3R','NWA-RD.HCSODA3DFS5','NWA-RD.HCSODA3JRA55']
N_hindc = len(simus_hindc)
dir_aviso = '/Volumes/P8/DART/AVISO/msla/ftp.sltac.cls.fr/Core/SEALEVEL_GLO_PHY_L4_REP_OBSERVATIONS_008_047/dataset-duacs-rep-global-merged-allsat-phy-l4-v3/monthly/'
N_interp=1000
N_months=len(datevec_simu_month)
ivar = 1
if (ivar == 0):
   prefix_image='GSpath'
else:
   prefix_image='GSpath2'

#########################################################################################
#%% Get data
#########################################################################################
print "Get data"
GS_paths_mat  = np.empty((N_months,N_members+N_hindc+1,N_interp,2))
GS_paths_mean = np.empty((N_months,N_interp,2))
GS_paths_stdc = np.empty((N_months,N_interp,2))
for iday,dday in enumerate(datevec_simu_month):
   print "Month : " + dday.strftime('%Y/%m')
   # Ensemble
   file_GS_paths = dir_obs+'GS_paths_'+dday.strftime('%Y%m')+'.nc'
   nc_GS_paths = ncdf.Dataset(file_GS_paths,'r')
   GS_paths_mat[iday,0:N_members,:,:] = nc_GS_paths.variables['GS_paths'][0,ivar,:]
   GS_paths_mean[iday,:,:]  = nc_GS_paths.variables['GS_paths_mean'][0,ivar,:]
   GS_paths_stdc[iday,:,:]  = nc_GS_paths.variables['GS_paths_stdc'][0,ivar,:]
   nc_GS_paths.close()
   # Hindcast
   file_GS_paths = dir_obs+'GS_paths_hind_'+dday.strftime('%Y%m')+'.nc'
   nc_GS_paths = ncdf.Dataset(file_GS_paths,'r')
   GS_paths_mat[iday,N_members:N_members+N_hindc,:,:] = nc_GS_paths.variables['GS_paths'][0,ivar,:]
   nc_GS_paths.close()
   # Aviso
   file_aviso_GS_paths = dir_aviso+'GS_paths_'+dday.strftime('%Y%m')+'.nc'
   nc_aviso_GS_paths = ncdf.Dataset(file_aviso_GS_paths,'r')
   GS_paths_mat[iday,N_members+N_hindc,:,:]  = nc_aviso_GS_paths.variables['GS_paths'][:]
   nc_aviso_GS_paths.close()

#########################################################################################
#%% Study on longitude axe
#########################################################################################
print "Longitude study"
lon_bins = np.arange(-78.125,-47.875,0.25)
lon_vec  = .5*(lon_bins[:-1]+lon_bins[1:])
lat_mean = np.empty((N_months,N_members+N_hindc+1,len(lon_vec)))
for iday,dday in enumerate(datevec_simu_month):
   for icur in xrange(N_members+N_hindc+1):
      idx_lato32 = GS_paths_mat[iday,icur,:,1]>32
      for ilon in xrange(len(lon_vec)):
         idx_lonbin = idx_lato32 & \
              (GS_paths_mat[iday,icur,:,0]>=lon_bins[ilon]) & (GS_paths_mat[iday,icur,:,0]<lon_bins[ilon+1])
         lat_mean[iday,icur,ilon] = GS_paths_mat[iday,icur,idx_lonbin,1].mean()
lat_mean_ensmean = lat_mean[:,0:N_members,:].mean(axis=1)
lat_mean_ensvar  = lat_mean[:,0:N_members,:].var(axis=1)


#sys.exit(0)

#########################################################################################
#%% Figures
#########################################################################################

fig = plt.figure(figsize=[9.,5.]);
for iday,dday in enumerate(datevec_simu_month):
   figname=dir_pictures + prefix_image+'_bylon_latvar_' + simu + '_' + dday.strftime('%Y%m')
   plt.clf()
   plt.plot(lon_vec,np.nanvar(lat_mean[iday,:],axis=0),'k')
   plt.ylim([0,1.3])
   plt.xlim([lon_vec[0],lon_vec[-1]])
   plt.xlabel('Longitude')
   plt.grid()
   plt.title('Latitude variance ('+dday.strftime('%Y/%m')+')',fontsize=20)
   rt_plotbox.set_plt_fontsize(plt.gca(),18)
   plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)
   plt.savefig(figname+'.png')
   print(figname+'.png')   

fig = plt.figure(figsize=[9.,5.]);
for iday,dday in enumerate(datevec_simu_month):
   figname=dir_pictures + prefix_image+'_bylon_' + simu + '_' + dday.strftime('%Y%m')
   plt.clf()
   plt.plot(lon_vec,lat_mean_ensmean[iday,:],'k',linewidth=2)
   plt.plot(lon_vec,lat_mean_ensmean[iday,:]+lat_mean_ensvar[iday,:],'k')
   plt.plot(lon_vec,lat_mean_ensmean[iday,:]-lat_mean_ensvar[iday,:],'k')
   plt.plot(lon_vec,lat_mean[iday,N_members+0,:],color=rt_colors['rust'],label=simus_hindc[0])
   plt.plot(lon_vec,lat_mean[iday,N_members+1,:],color=rt_colors['applered'],label=simus_hindc[1])
   plt.plot(lon_vec,lat_mean[iday,N_members+2,:],color=rt_colors['killarney'],label=simus_hindc[2])
   plt.plot(lon_vec,lat_mean[iday,N_members+N_hindc,:],'b',linewidth=2)
   plt.ylim([32,42])
   plt.xlim([lon_vec[0],lon_vec[-1]])
   plt.xlabel('Longitude')
   plt.grid()
   plt.title('Latitude of GS path ('+dday.strftime('%Y/%m')+')',fontsize=20)
   rt_plotbox.set_plt_fontsize(plt.gca(),18)
   plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)
   plt.savefig(figname+'.png')
   print(figname+'.png')   

fds = mpl_dates.date2num(datevec_simu_month)

Nmax_lon=120
fig = plt.figure(figsize=[15.,7.]);
rmse_ens = np.sqrt(np.nanmean((lat_mean_ensmean[:,0:Nmax_lon]-lat_mean[:,N_members+N_hindc,0:Nmax_lon])**2,axis=1))
plt.plot(fds,rmse_ens,label='Ensemble',linewidth=2)
for ihind in xrange(N_hindc):
   rmse_hind = np.sqrt(np.nanmean((lat_mean[:,N_members+ihind,0:Nmax_lon]-lat_mean[:,N_members+N_hindc,0:Nmax_lon])**2,axis=1))
   plt.plot(fds,rmse_hind,label=simus_hindc[ihind])
plt.xlim([fds[0],fds[-1]])
plt.ylim([0,2.5])
rt_plotbox.xaxis_date(fds,step='month',date_format='%b')
rt_plotbox.set_plt_fontsize(plt.gca(),18)
plt.title('Evolution of RMSE for latitude of GS',fontsize=20)
plt.legend()
plt.grid()
rt_plotbox.set_plt_fontsize(plt.gca(),18)
plt.subplots_adjust(left=0.05, right=0.95, top=0.93, bottom=0.1)
figname=dir_pictures +prefix_image+'_RMSE_evol.png'
plt.savefig(figname)
print(figname)

Nmax_lon=73
fig = plt.figure(figsize=[15.,7.]);
rmse_ens = np.sqrt(np.nanmean((lat_mean_ensmean[:,0:Nmax_lon]-lat_mean[:,N_members+N_hindc,0:Nmax_lon])**2,axis=1))
plt.plot(fds,rmse_ens,label='Ensemble',linewidth=2)
for ihind in xrange(N_hindc):
   rmse_hind = np.sqrt(np.nanmean((lat_mean[:,N_members+ihind,0:Nmax_lon]-lat_mean[:,N_members+N_hindc,0:Nmax_lon])**2,axis=1))
   plt.plot(fds,rmse_hind,label=simus_hindc[ihind])
plt.xlim([fds[0],fds[-1]])
plt.ylim([0,2.5])
rt_plotbox.xaxis_date(fds,step='month',date_format='%b')
rt_plotbox.set_plt_fontsize(plt.gca(),18)
plt.title('Evolution of RMSE for latitude of GS (80W-60W)',fontsize=20)
plt.legend()
plt.grid()
rt_plotbox.set_plt_fontsize(plt.gca(),18)
plt.subplots_adjust(left=0.05, right=0.95, top=0.93, bottom=0.1)
figname=dir_pictures +prefix_image+'_RMSE_GS_evol_60W.png'
plt.savefig(figname)
print(figname)

Nmax_lon=50
fig = plt.figure(figsize=[15.,7.]);
rmse_ens = np.sqrt(np.nanmean((lat_mean_ensmean[:,0:Nmax_lon]-lat_mean[:,N_members+N_hindc,0:Nmax_lon])**2,axis=1))
plt.plot(fds,rmse_ens,label='Ensemble',linewidth=2)
for ihind in xrange(N_hindc):
   rmse_hind = np.sqrt(np.nanmean((lat_mean[:,N_members+ihind,0:Nmax_lon]-lat_mean[:,N_members+N_hindc,0:Nmax_lon])**2,axis=1))
   plt.plot(fds,rmse_hind,label=simus_hindc[ihind])
plt.xlim([fds[0],fds[-1]])
plt.ylim([0,2])
rt_plotbox.xaxis_date(fds,step='month',date_format='%b')
rt_plotbox.set_plt_fontsize(plt.gca(),18)
plt.title('Evolution of RMSE for latitude of GS (80W-65W)',fontsize=20)
plt.legend()
plt.grid()
rt_plotbox.set_plt_fontsize(plt.gca(),18)
plt.subplots_adjust(left=0.05, right=0.95, top=0.93, bottom=0.1)
figname=dir_pictures +prefix_image+'_RMSE_GS_evol_65W.png'
plt.savefig(figname)
print(figname)

fig = plt.figure(figsize=[15.,7.]);
rmse_ens = np.sqrt(np.nanmean((lat_mean_ensmean[6:,:]-lat_mean[6:,N_members+N_hindc,:])**2,axis=0))
plt.plot(lon_vec,rmse_ens,label='Ensemble mean',linewidth=2)
for ihind in xrange(N_hindc):
   rmse_hind = np.sqrt(np.nanmean((lat_mean[6:,N_members+ihind,:]-lat_mean[6:,N_members+N_hindc,:])**2,axis=0))
   plt.plot(lon_vec,rmse_hind,label=simus_hindc[ihind])
plt.xlim([lon_vec[0],lon_vec[-1]])
plt.xlabel('Longitude')
plt.grid()
plt.legend()
plt.title('Time averaged RMSE for latitude of GS',fontsize=20)
rt_plotbox.set_plt_fontsize(plt.gca(),18)
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)
figname=dir_pictures +prefix_image+'_RMSE_bylon.png'
plt.savefig(figname+'.png')
print(figname+'.png')

#fig = plt.figure(figsize=[18.,10.]);
#for iday,dday in enumerate(datevec_simu_month):
#   figname=dir_pictures + prefix_image+'_allVSavisoVShind_mean_' + simu + '_' + dday.strftime('%Y%m')
#   plt.clf()
#   m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),fontsiz=25,\
#        plotitle='GS path ('+dday.strftime('%Y/%m')+')',geo=[-85,-48,25,45],\
#        stepX=5.,stepY=5)
#   for imem in xrange(N_members):
#      plt.plot(GS_paths_mat[iday,imem,:,0],GS_paths_mat[iday,imem,:,1],color=[.5,.5,.5])
#   # AVISO
#   plt.plot(GS_paths_mat[iday,N_members+N_hindc,:,0],  GS_paths_mat[iday,N_members+N_hindc,:,1],\
#         linewidth=2,color=rt_colors['hyperblue'],label='AVISO')
#   # Hindcast
#   plt.plot(GS_paths_mat[iday,N_members,:,0],  GS_paths_mat[iday,N_members,:,1],color=rt_colors['rust'],label=simus_hindc[0])
#   plt.plot(GS_paths_mat[iday,N_members+1,:,0],GS_paths_mat[iday,N_members+1,:,1],color=rt_colors['applered'],label=simus_hindc[1])
#   plt.plot(GS_paths_mat[iday,N_members+2,:,0],GS_paths_mat[iday,N_members+2,:,1],color=rt_colors['killarney'],label=simus_hindc[2])
#   # Mean and std
#   plt.plot(GS_paths_mean[iday,:,0],GS_paths_mean[iday,:,1],color='k',linewidth=2)
#   plt.plot(GS_paths_mean[iday,:,0]+GS_paths_stdc[iday,:,0],GS_paths_mean[iday,:,1]+GS_paths_stdc[iday,:,1],color='k')
#   plt.plot(GS_paths_mean[iday,:,0]-GS_paths_stdc[iday,:,0],GS_paths_mean[iday,:,1]-GS_paths_stdc[iday,:,1],color='k')
#   plt.legend(loc='upper left')
#   plt.savefig(figname+'.png')
#   print(figname+'.png')

fig = plt.figure(figsize=[18.,10.]);
for iday,dday in enumerate(datevec_simu_month):
   figname=dir_pictures + prefix_image+'_allVSavisoVShind_' + simu + '_' + dday.strftime('%Y%m')
   plt.clf()
   m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),fontsiz=25,\
        plotitle='GS path ('+dday.strftime('%Y/%m')+')',geo=[-85,-48,25,45],\
        stepX=5.,stepY=5)
   for imem in xrange(N_members):
      plt.plot(GS_paths_mat[iday,imem,:,0],GS_paths_mat[iday,imem,:,1],color=[.5,.5,.5])
   # AVISO
   plt.plot(GS_paths_mat[iday,N_members+N_hindc,:,0],  GS_paths_mat[iday,N_members+N_hindc,:,1],\
         linewidth=2,color=rt_colors['hyperblue'],label='AVISO')
   # Hindcast
   plt.plot(GS_paths_mat[iday,N_members,:,0],  GS_paths_mat[iday,N_members,:,1],color=rt_colors['rust'],label=simus_hindc[0])
   plt.plot(GS_paths_mat[iday,N_members+1,:,0],GS_paths_mat[iday,N_members+1,:,1],color=rt_colors['applered'],label=simus_hindc[1])
   plt.plot(GS_paths_mat[iday,N_members+2,:,0],GS_paths_mat[iday,N_members+2,:,1],color=rt_colors['killarney'],label=simus_hindc[2])
   plt.legend(loc='upper left',fontsize=20)
   plt.savefig(figname+'.png')
   print(figname+'.png')

sel_dates_idx = [0,2,5,7,9,11,13,15,17]


fig = plt.figure(figsize=[23.,17.]);
plt.clf()
figname=dir_pictures + prefix_image+'_allVSavisoVShind_' + simu + '_seldates'
for icur,iday in enumerate(sel_dates_idx):
   dday = datevec_simu_month[iday]
   m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),fontsiz=20,geo=[-82,-55,25,45],\
        stepX=5.,stepY=5,subpltid=(3,3,icur+1))

   for imem in xrange(N_members):
      plt.plot(GS_paths_mat[iday,imem,:,0],GS_paths_mat[iday,imem,:,1],color=[.5,.5,.5])
   # AVISO
   plt.plot(GS_paths_mat[iday,N_members+N_hindc,:,0],  GS_paths_mat[iday,N_members+N_hindc,:,1],\
         linewidth=3,color=rt_colors['hyperblue'],label='AVISO')
   # Hindcast
   plt.plot(GS_paths_mat[iday,N_members,:,0],  GS_paths_mat[iday,N_members,:,1],color=rt_colors['rust'],label=simus_hindc[0])
   plt.plot(GS_paths_mat[iday,N_members+1,:,0],GS_paths_mat[iday,N_members+1,:,1],color=rt_colors['applered'],label=simus_hindc[1])
   plt.plot(GS_paths_mat[iday,N_members+2,:,0],GS_paths_mat[iday,N_members+2,:,1],color=rt_colors['killarney'],label=simus_hindc[2])
   if (icur == 0):
      plt.legend(loc='lower right',fontsize=20)
   plt.text(-68,43,dday.strftime('%b %Y'),bbox=dict(facecolor='white',edgecolor='white'),fontsize=25,horizontalalignment='center')
plt.subplots_adjust(left=0.05, right=0.97, top=0.98, bottom=0.03,wspace=0.2,hspace=0.15)
plt.savefig(figname+'.png')
print(figname+'.png')


sys.exit(0)

fig = plt.figure(figsize=[18.,10.]);
for iday,dday in enumerate(datevec_simu_month):
   figname=dir_pictures + prefix_image+'_all_mean_bathyC_' + simu + '_' + dday.strftime('%Y%m')
   plt.clf()
   m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),fontsiz=25,\
        plotitle='GS path ('+dday.strftime('%Y/%m')+')',geo=[-85,-48,25,45],\
        stepX=5.,stepY=5)
   CS=plt.contour(lon_rho,lat_rho,RomsGrid.grid.variables['h'].value,[200,500,1000,1500,2000,3000,4000,5000],\
                 cmap=plt.get_cmap('Greys_r'),vmin=-1000,vmax=6000)
   plt.clabel(CS, fontsize=14, inline=1, )
   for imem in xrange(N_members):
      plt.plot(GS_paths_mat[iday,imem,:,0],GS_paths_mat[iday,imem,:,1],color=[.5,.5,.5])
   plt.plot(GS_paths_mean[iday,:,0],GS_paths_mean[iday,:,1],color='k',linewidth=2)
   plt.plot(GS_paths_mean[iday,:,0]+GS_paths_stdc[iday,:,0],GS_paths_mean[iday,:,1]+GS_paths_stdc[iday,:,1],color='k')
   plt.plot(GS_paths_mean[iday,:,0]-GS_paths_stdc[iday,:,0],GS_paths_mean[iday,:,1]-GS_paths_stdc[iday,:,1],color='k')
   plt.savefig(figname+'.png')
   print(figname+'.png')


fig = plt.figure(figsize=[18.,10.]);
for iday,dday in enumerate(datevec_simu_month):
   figname=dir_pictures + prefix_image+'_allVShind_' + simu + '_' + dday.strftime('%Y%m')
   plt.clf()
   m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),fontsiz=25,\
        plotitle='GS path ('+dday.strftime('%Y/%m')+')',geo=[-85,-48,25,45],\
        stepX=5.,stepY=5)
   for imem in xrange(N_members):
      plt.plot(GS_paths_mat[iday,imem,:,0],GS_paths_mat[iday,imem,:,1],color=[.5,.5,.5])
   plt.plot(GS_paths_mat[iday,N_members,:,0],  GS_paths_mat[iday,N_members,:,1],color=rt_colors['rust'],label=simus_hindc[0])
   plt.plot(GS_paths_mat[iday,N_members+1,:,0],GS_paths_mat[iday,N_members+1,:,1],color=rt_colors['applered'],label=simus_hindc[1])
   plt.plot(GS_paths_mat[iday,N_members+2,:,0],GS_paths_mat[iday,N_members+2,:,1],color=rt_colors['killarney'],label=simus_hindc[2])
   plt.legend(loc='lower right')
   plt.savefig(figname+'.png')
   print(figname+'.png')

fig = plt.figure(figsize=[18.,10.]);
for iday,dday in enumerate(datevec_simu_month):
   figname=dir_pictures + prefix_image+'_allVShind_bathyC_' + simu + '_' + dday.strftime('%Y%m')
   plt.clf()
   m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),fontsiz=25,\
        plotitle='GS path ('+dday.strftime('%Y/%m')+')',geo=[-85,-48,25,45],\
        stepX=5.,stepY=5)
   CS=plt.contour(lon_rho,lat_rho,RomsGrid.grid.variables['h'].value,[200,500,1000,1500,2000,3000,4000,5000],\
                 cmap=plt.get_cmap('Greys_r'),vmin=-1000,vmax=6000)
   plt.clabel(CS, fontsize=14, inline=1, )
   for imem in xrange(N_members):
      plt.plot(GS_paths_mat[iday,imem,:,0],GS_paths_mat[iday,imem,:,1],color=[.5,.5,.5])
   plt.plot(GS_paths_mat[iday,N_members,:,0],  GS_paths_mat[iday,N_members,:,1],color=rt_colors['rust'],label=simus_hindc[0])
   plt.plot(GS_paths_mat[iday,N_members+1,:,0],GS_paths_mat[iday,N_members+1,:,1],color=rt_colors['applered'],label=simus_hindc[1])
   plt.plot(GS_paths_mat[iday,N_members+2,:,0],GS_paths_mat[iday,N_members+2,:,1],color=rt_colors['killarney'],label=simus_hindc[2])
   plt.legend()
   plt.savefig(figname+'.png')
   print(figname+'.png')








