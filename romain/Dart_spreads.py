# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 14:34:00 2016

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


spread_temp_prior=np.zeros([N_days_simu,1])
spread_temp_poste=np.zeros([N_days_simu,1])
spread_sst_prior=np.zeros([N_days_simu,1])
spread_sst_poste=np.zeros([N_days_simu,1])
spread_salt_prior=np.zeros([N_days_simu,1])
spread_salt_poste=np.zeros([N_days_simu,1])
spread_sss_prior=np.zeros([N_days_simu,1])
spread_sss_poste=np.zeros([N_days_simu,1])

for i_cur,i_date in enumerate(range(N_days)):
    mydate=start_assim+dtime.timedelta(i_date)
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
