# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 14:12:32 2016

@author: romain
"""

print('----------------------------------------------------------------')
print('                        Post-processing Obs Dart                ')
print('----------------------------------------------------------------')

#%% Toolboxes

from param_dart import *

#%% Observations

i_start = (start_assim - start_simu).days -1
i_final = (final_assim - start_simu).days -1


fig = plt.figure(figsize=[20.,15.])
for i_day in np.arange(i_start,i_final+1):
    # Get data
    file_obs = dir_obs_diag+'obs_seq.sst1.'+str(i_day).zfill(3)+'.nc';
    nc_obs = ncdf.Dataset(file_obs,'r')
    
    obs_lon     = np.array(nc_obs.variables['location'])[:,0]-360
    obs_lat     = np.array(nc_obs.variables['location'])[:,1]
    obs_val     = np.array(nc_obs.variables['observations'])[:,0]
    obs_prior   = np.array(nc_obs.variables['observations'])[:,1]
    obs_spread  = np.array(nc_obs.variables['observations'])[:,3]
    obs_qc      = np.array(nc_obs.variables['qc'])[:,1]
    
    nc_obs.close()
    
    obs_prior[obs_prior>1000]=float('nan')
    obs_spread[obs_spread>1000]=float('nan')
    
    plt.clf()
    m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),subpltid=221,fontsiz=14,plotitle='Observations')
    m.scatter(obs_lon, obs_lat, c=obs_val,edgecolors='none',s=10,cmap=rt_colormaps['intense2'])
    cb=m.colorbar(pad="8%")
    m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),subpltid=222,fontsiz=14,plotitle='Spread')
    m.scatter(obs_lon, obs_lat, c=obs_spread,edgecolors='none',s=10,cmap=rt_colormaps['eke2'])
    cb=m.colorbar(pad="8%")
    m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),subpltid=223,fontsiz=14,plotitle='Dart QC')
    m.scatter(obs_lon, obs_lat, c=obs_qc,edgecolors='none',s=10)
    cb=m.colorbar(pad="8%")
    m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),subpltid=224,fontsiz=14,plotitle='Innovation')
    m.scatter(obs_lon, obs_lat,c=obs_val-obs_prior,edgecolors='none',s=10,cmap=rt_colormaps['redblueclass'],vmin=-5,vmax=5)
    cb=m.colorbar(pad="8%")
    figname=dir_pictures + '/Obs_seq_out_' + simu + '_' + (start_simu+dtime.timedelta(i_day)).strftime('%Y%m%d') + '.png'
    plt.savefig(figname)
    print(figname)

    
    

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
    
spread_temp_prior=np.zeros([N_days_simu,1])
spread_temp_poste=np.zeros([N_days_simu,1])
spread_sst_prior=np.zeros([N_days_simu,1])
spread_sst_poste=np.zeros([N_days_simu,1])
spread_salt_prior=np.zeros([N_days_simu,1])
spread_salt_poste=np.zeros([N_days_simu,1])
spread_sss_prior=np.zeros([N_days_simu,1])
spread_sss_poste=np.zeros([N_days_simu,1])

for i_cur,i_date in enumerate(range(N_days_simu)):
    mydate=start_simu+dtime.timedelta(i_date)
    print(mydate.strftime('%Y/%m/%d'))
    prio_diag_file = dir_obs_diag+'Prior_Diag_'    +mydate.strftime('%Y%m%d')+'.nc';
    post_diag_file = dir_obs_diag+'Posterior_Diag_'+mydate.strftime('%Y%m%d')+'.nc';
    
    nc_prio = ncdf.Dataset(prio_diag_file,'r')
    prio_temp = nc_prio.variables['temp'][0,0,39,:,:]
    prio_temp_sp = nc_prio.variables['temp'][0,1,:,:,:];
    prio_temp_sp=np.ma.masked_where(np.tile(mask,[40,1,1])==0,prio_temp_sp);
    prio_salt_sp = nc_prio.variables['salt'][0,1,:,:,:];
    prio_salt_sp=np.ma.masked_where(np.tile(mask,[40,1,1])==0,prio_salt_sp);
    spread_temp_prior[i_cur]=np.mean(prio_temp_sp);
    spread_sst_prior[i_cur]=np.mean(prio_temp_sp[39,:,:]);
    spread_salt_prior[i_cur]=np.mean(prio_salt_sp);
    spread_sss_prior[i_cur]=np.mean(prio_salt_sp[39,:,:]);
    nc_prio.close()
    
    if mydate>=start_assim:
        nc_post = ncdf.Dataset(post_diag_file,'r')
        post_temp = nc_post.variables['temp'][0,0,39,:,:]
        post_temp_sp = nc_post.variables['temp'][0,1,:,:,:]
        post_temp_sp=np.ma.masked_where(np.tile(mask,[40,1,1])==0,post_temp_sp);
        post_salt_sp = nc_post.variables['salt'][0,1,:,:,:]
        post_salt_sp=np.ma.masked_where(np.tile(mask,[40,1,1])==0,post_salt_sp);
        spread_temp_poste[i_cur]=np.mean(post_temp_sp);
        spread_sst_poste[i_cur]=np.mean(post_temp_sp[39,:,:]);    
        spread_salt_poste[i_cur]=np.mean(post_salt_sp);
        spread_sss_poste[i_cur]=np.mean(post_salt_sp[39,:,:]);
        nc_post.close()
    
spread_temp_poste = np.ma.masked_where(spread_temp_poste == 0,spread_temp_poste)
spread_sst_poste  = np.ma.masked_where(spread_sst_poste  == 0,spread_sst_poste )
spread_salt_poste = np.ma.masked_where(spread_salt_poste == 0,spread_salt_poste)
spread_sss_poste  = np.ma.masked_where(spread_sss_poste  == 0,spread_sss_poste )


datevec_assim=[start_assim+dtime.timedelta(i_date) for i_date in range(N_days)]
datevec_simu=[start_simu+dtime.timedelta(i_date) for i_date in range(N_days_simu)]
fds = mpl_dates.date2num(datevec_assim) # converted
fds_simu = mpl_dates.date2num(datevec_simu) # converted

date_step=10

fig = plt.figure(figsize=[20.,15.]);plt.clf()
ax=fig.add_subplot(221)
p=plt.plot(fds_simu,spread_sst_prior,'k-o')
plt.plot(fds_simu,spread_sst_poste,'r-o')
rt_plotbox.xaxis_date(fds_simu,ax=ax,step=date_step,date_format='%m/%d')
ax.set_ylim(bottom=0,top=0.6)
plt.grid(which='both')
plt.title('Spread SST')
ax=fig.add_subplot(222)
p=plt.plot(fds_simu,spread_temp_prior,'k-o')
plt.plot(fds_simu,spread_temp_poste,'r-o')
rt_plotbox.xaxis_date(fds_simu,ax=ax,step=date_step,date_format='%m/%d')
ax.set_ylim(bottom = 0,top=0.6)
plt.grid(which='both')
plt.title('Spread Temp')
ax=fig.add_subplot(223)
p=plt.plot(fds_simu,spread_sss_prior,'k-o')
plt.plot(fds_simu,spread_sss_poste,'r-o')
rt_plotbox.xaxis_date(fds_simu,ax=ax,step=date_step,date_format='%m/%d')
ax.set_ylim(bottom = 0,top=0.6)
plt.grid(which='both')
plt.title('Spread SSS')
ax=fig.add_subplot(224)
p=plt.plot(fds_simu,spread_salt_prior,'k-o')
plt.plot(fds_simu,spread_salt_poste,'r-o')
rt_plotbox.xaxis_date(fds_simu,ax=ax,step=date_step,date_format='%m/%d')
ax.set_ylim(bottom = 0,top=0.6)
plt.grid(which='both')
plt.title('Spread Salt')
figname=dir_pictures + '/Spreads_' + simu + '.png'
plt.savefig(figname)
print(figname)


#%% Spread

#spread_prior=np.zeros([N_days,1])
#spread_poste=np.zeros([N_days,1])
#
#for i_cur,i_day in enumerate(np.arange(i_start,i_final+1)):
#    file_obs = dir_obs_diag+'obs_seq.sst1.'+str(i_day).zfill(3)+'.nc';
#    nc_obs = ncdf.Dataset(file_obs,'r')
#    
#    obs_qc      = np.array(nc_obs.variables['qc'])[:,1]
#    obs_prior   = np.array(nc_obs.variables['observations'])[obs_qc==0,5:64:2]
#    obs_poste   = np.array(nc_obs.variables['observations'])[obs_qc==0,6:66:2]
#
#    spread_prior[i_cur]=np.mean(rt_dart_tools.dart_spread(obs_prior));
#    spread_poste[i_cur]=np.mean(rt_dart_tools.dart_spread(obs_poste));
#
#datevec_assim=[start_assim+dtime.timedelta(i_date) for i_date in range(N_days)]
#fds = mpl_dates.date2num(datevec_assim) # converted
#date_step=3
#
#fig = plt.figure(figsize=[10.,7.]);plt.clf()
#ax=fig.add_subplot(111)
#p=plt.plot(fds,spread_prior,'k-o')
#plt.plot(fds,spread_poste,'r-o')
#rt_plotbox.xaxis_date(fds,ax=ax,step=2,date_format='%m/%d')
#ax.set_ylim(bottom = 0)
#plt.grid(which='both')
#plt.title('Spread')




#%% Diagnosis

file_obs_diag = dir_obs_diag+'obs_diag_output.nc'
nc_diags = ncdf.Dataset(file_obs_diag,'r')
date_vec = [dtime.datetime(1601,1,1)+dtime.timedelta(dt) for dt in nc_diags.variables['time'][:]]

rank_his = np.squeeze(np.array(nc_diags.variables['SATELLITE_INFRARED_SST_guess_RankHist'])[:])
diag_prio = np.squeeze(np.array(nc_diags.variables['SATELLITE_INFRARED_SST_guess'])[:])
diag_prio  = np.ma.masked_where(diag_prio < -80000,diag_prio )
diag_post = np.squeeze(np.array(nc_diags.variables['SATELLITE_INFRARED_SST_analy'])[:])
diag_post  = np.ma.masked_where(diag_post < -80000,diag_post )

nc_diags.close()

#date_2D,bin_2D  = np.meshgrid(np.arange(N_days_simu),np.arange(31))
#x_bar=date_2D.flatten()
#y_bar=bin_2D.flatten()
#z_bar=np.zeros_like(x_bar)
#dx_bar = 0.5 * np.ones_like(z_bar)
#dy_bar = dx_bar.copy()
#dz_bar = (rank_his.T).flatten()
#
#from mpl_toolkits.mplot3d import Axes3D
#fig = plt.figure(figsize=[10.,7.]);plt.clf()
#ax1 = fig.add_subplot(111, projection='3d')
#ax1.bar3d(x_bar, y_bar, z_bar, dx_bar, dy_bar, dz_bar, color='#00ceaa')
#ax1.view_init(elev=25, azim=25)
#plt.show()

fig = plt.figure(figsize=[15.,15.]);plt.clf()
fds = mpl_dates.date2num(date_vec) # converted
date_step=10

ax1 = fig.add_subplot(221)
ax1.plot(fds, diag_prio[:,6], 'k-*',label='Prior')
ax1.plot(fds, diag_post[:,6], 'r-*',label='Posterior')
ax1.set_ylim(bottom = 0, top = 5)
ax1.set_title('RMSE', color='k')
ax1.set_xlabel('time', color='k')
rt_plotbox.xaxis_date(fds,ax=ax1,step=date_step,date_format='%m/%d')
ax2 = ax1.twinx()
ax2.plot(fds, diag_post[:,0], 'o', markerfacecolor='w',markeredgecolor='b')
ax2.plot(fds, diag_post[:,1], 'b+')
ax2.set_ylim(top = 15000)
ax2.set_ylabel('# of obs : o=possible, +=assimilated', color='b')
for tl in ax2.get_yticklabels():
    tl.set_color('b')
ax1.set_xlim(left=mpl_dates.date2num(start_assim)-2,right=mpl_dates.date2num(final_assim)-1)
ax1.grid()
h1, l1 = ax1.get_legend_handles_labels()
ax2.legend(h1,l1,fancybox=True)


ax1 = fig.add_subplot(222)
ax1.plot(fds, diag_prio[:,7], 'k-*')
ax1.plot(fds, diag_post[:,7], 'r-*')
ax1.set_ylim(bottom = 0, top = 2.5)
ax1.set_title('Bias', color='k')
ax1.set_xlabel('time', color='k')
rt_plotbox.xaxis_date(fds,ax=ax1,step=date_step,date_format='%m/%d')
ax1.set_xlim(left=mpl_dates.date2num(start_assim)-2,right=mpl_dates.date2num(final_assim)-1)
ax1.grid()

ax1 = fig.add_subplot(223)
ax1.plot(fds, diag_prio[:,8], 'k-*')
ax1.plot(fds, diag_post[:,8], 'r-*')
ax1.set_ylim(bottom = 0, top = 0.9)
ax1.set_title('Spread', color='k')
ax1.set_xlabel('time', color='k')
rt_plotbox.xaxis_date(fds,ax=ax1,step=date_step,date_format='%m/%d')
ax1.set_xlim(left=mpl_dates.date2num(start_assim)-2,right=mpl_dates.date2num(final_assim)-1)
ax1.grid()

ax1 = fig.add_subplot(224)
ax1.plot(fds, diag_prio[:,11], 'k-*')
ax1.plot(fds, diag_prio[:,12], 'k-o')
ax1.plot(fds, diag_post[:,11], 'r-*')
ax1.plot(fds, diag_post[:,12], 'r-o')
ax1.set_title('*=Obs o=Model', color='k')
ax1.set_xlabel('time', color='k')
rt_plotbox.xaxis_date(fds,ax=ax1,step=date_step,date_format='%m/%d')
ax1.set_xlim(left=mpl_dates.date2num(start_assim)-2,right=mpl_dates.date2num(final_assim)-1)
ax1.grid()

figname=dir_pictures + '/Diags_' + simu + '.eps'
plt.savefig(figname)
print(figname)




